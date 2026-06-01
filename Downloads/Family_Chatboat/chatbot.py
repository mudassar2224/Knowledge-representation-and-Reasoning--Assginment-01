# Natural-language dispatcher for the Family Knowledge Base Chatbot.

import re

from aiml_bot import get_aiml_response
from prolog_engine import query, query_yes_no
from utils import (
    KNOWN_NAMES,
    PROPERTY_RELATIONS,
    RELATION_MAP,
    RELATION_NAMES,
    capitalize_name,
    clean_text,
    extract_names,
    find_relation,
    format_response,
    format_value,
    format_yes_no,
    is_safe_atom,
    label_for,
    normalize_atom,
    words,
)


AIML_ONLY_PATTERNS = [
    r"^(hi|hello|hey|greetings|good morning|good evening|good afternoon|salam|assalam o alaikum)$",
    r"^(bye|goodbye|see you|take care|Allah hafiz|allah hafiz)$",
    r"^(help|what can you do|how do i use this|how do i use)$",
]

KNOWN_CITIES = {"lahore", "karachi", "islamabad", "peshawar"}
KNOWN_OCCUPATIONS = {
    "doctor", "teacher", "engineer", "nurse", "lawyer", "accountant",
    "businessman", "professor", "principal", "pilot", "student",
}

UNARY_RELATIONS = {"male", "female"}


def handle_input(user_input):
    user_input = user_input.strip()
    if not user_input:
        return "Please type a question."

    if _is_aiml_intent(user_input):
        response = get_aiml_response(user_input)
        if response:
            return response

    return _prolog_dispatch(user_input)


def _is_aiml_intent(text):
    cleaned = clean_text(text)
    return any(re.match(pattern, cleaned, re.IGNORECASE) for pattern in AIML_ONLY_PATTERNS)


def _dedupe(raw, var="X"):
    """Extract unique values from mixed Pytholog result shapes."""
    seen = set()
    values = []
    for item in raw or []:
        value = ""
        if isinstance(item, dict):
            value = item.get(var, "")
            if not value and item:
                value = next(iter(item.values()))
        elif isinstance(item, str) and item.lower() not in {"yes", "no", "false"}:
            value = item

        value = str(value).strip()
        if value and value not in seen:
            seen.add(value)
            values.append(value)
    return values


def _prolog_dispatch(text):
    cleaned = clean_text(text)
    if not cleaned:
        return "Please type a question."

    names = extract_names(cleaned)

    yes_no = _answer_yes_no(cleaned, names)
    if yes_no:
        return yes_no

    unary_status = _answer_unary_status(cleaned)
    if unary_status:
        return unary_status

    gender_list = _answer_gender_list(cleaned)
    if gender_list:
        return gender_list

    family_list = _answer_family_member_list(cleaned)
    if family_list:
        return family_list

    if _looks_like_profile_request(cleaned) and names:
        return _all_about(names[0])

    relation = find_relation(cleaned)

    if relation in PROPERTY_RELATIONS and names:
        return _answer_property(relation, names[0])

    if relation and relation in RELATION_NAMES and names:
        return _answer_relationship(relation, names[0])

    grouped_answer = _answer_same_group(cleaned, names)
    if grouped_answer:
        return grouped_answer

    city_answer = _answer_city_list(cleaned)
    if city_answer:
        return city_answer

    all_members = _answer_all_members(cleaned)
    if all_members:
        return all_members

    occupation_answer = _answer_occupation_list(cleaned)
    if occupation_answer:
        return occupation_answer

    if len(names) == 1:
        return _all_about(names[0])

    return _fallback()


def _answer_yes_no(text, names):
    # "is shakeel an ancestor of zain"
    m = re.search(r"\bis\s+(\w+)\s+(?:a|an|the)?\s*(.+?)\s+(?:of|to|for)\s+(\w+)\b", text)
    if m:
        x = normalize_atom(m.group(1))
        relation = find_relation(m.group(2))
        y = normalize_atom(m.group(3))
        if relation in RELATION_NAMES:
            if x not in KNOWN_NAMES or y not in KNOWN_NAMES:
                missing = [capitalize_name(name) for name in (x, y) if name not in KNOWN_NAMES]
                if missing:
                    return f"Sorry, I do not have {', '.join(missing)} in this family KB."
            if _valid_person_pair(x, y):
                return format_yes_no(relation, x, y, query_yes_no(relation, [x, y]))

    # "is ali male" / "is ali female"
    m = re.search(r"\bis\s+(\w+)\s+(?:a|an\s+)?(male|female)\b", text)
    if m:
        person = normalize_atom(m.group(1))
        relation = normalize_atom(m.group(2))
        if person in KNOWN_NAMES:
            result = bool(query(relation, [person]))
            if result:
                return f"Yes, {capitalize_name(person)} is {relation}."
            return f"No, {capitalize_name(person)} is not {relation}."

    # "is ali married"
    m = re.search(r"\bis\s+(\w+)\s+married\b(?!\s+(?:to|with|for))", text)
    if m:
        person = normalize_atom(m.group(1))
        if person in KNOWN_NAMES:
            result = bool(query("spouse", [person, "X"])) or bool(query("married", [person, "X"]))
            if result:
                return f"Yes, {capitalize_name(person)} is married."
            return f"No, {capitalize_name(person)} is not married."

    # "are ali and alia married"
    m = re.search(r"\bare\s+(\w+)\s+and\s+(\w+)\s+married\b", text)
    if m:
        x, y = normalize_atom(m.group(1)), normalize_atom(m.group(2))
        if _valid_person_pair(x, y):
            return format_yes_no("spouse", x, y, query_yes_no("spouse", [x, y]))

    # "is ali related to asad"
    m = re.search(r"\bis\s+(\w+)\s+related\s+to\s+(\w+)\b", text)
    if m:
        x, y = normalize_atom(m.group(1)), normalize_atom(m.group(2))
        if _valid_person_pair(x, y):
            return format_yes_no("blood_relative", x, y, query_yes_no("blood_relative", [x, y]))

    # "are ali and asad related"
    m = re.search(r"\bare\s+(\w+)\s+and\s+(\w+)\s+(?:related|blood relatives|relatives)\b", text)
    if m:
        x, y = normalize_atom(m.group(1)), normalize_atom(m.group(2))
        if _valid_person_pair(x, y):
            return format_yes_no("blood_relative", x, y, query_yes_no("blood_relative", [x, y]))

    # "does ali live in lahore"
    m = re.search(r"\bdoes\s+(\w+)\s+(?:live|lives|reside)\s+(?:in|at)\s+(\w+)\b", text)
    if m:
        person, city = normalize_atom(m.group(1)), normalize_atom(m.group(2))
        if person in KNOWN_NAMES and city in KNOWN_CITIES:
            result = query_yes_no("lives_in", [person, city])
            return _property_yes_no("lives in", person, city, result)

    # "is ali from lahore"
    m = re.search(r"\bis\s+(\w+)\s+from\s+(\w+)\b", text)
    if m:
        person, city = normalize_atom(m.group(1)), normalize_atom(m.group(2))
        if person in KNOWN_NAMES and city in KNOWN_CITIES:
            result = query_yes_no("lives_in", [person, city])
            return _property_yes_no("from", person, city, result)

    # "is ali a doctor"
    m = re.search(r"\bis\s+(\w+)\s+(?:a|an)\s+(\w+)\b", text)
    if m:
        person, occupation = normalize_atom(m.group(1)), _singular(normalize_atom(m.group(2)))
        if person in KNOWN_NAMES and occupation in KNOWN_OCCUPATIONS:
            result = query_yes_no("occupation", [person, occupation])
            return _property_yes_no("a", person, occupation, result)

    # "does ali have siblings"
    m = re.search(r"\bdoes\s+(\w+)\s+have\s+(.+)\b", text)
    if m:
        person = normalize_atom(m.group(1))
        relation = find_relation(m.group(2))
        if person in KNOWN_NAMES and relation in RELATION_NAMES:
            results = _dedupe(query(relation, ["X", person]))
            return f"Yes, {capitalize_name(person)} has {label_for(relation)}." if results else (
                f"No, I could not find any {label_for(relation)} for {capitalize_name(person)}."
            )

    return None


def _answer_unary_status(text):
    m = re.search(r"\bis\s+(\w+)\s+(?:a|an\s+)?(male|female)\b", text)
    if not m:
        return None

    person = normalize_atom(m.group(1))
    relation = normalize_atom(m.group(2))
    if person not in KNOWN_NAMES or relation not in UNARY_RELATIONS:
        return None

    result = bool(query(relation, [person]))
    if result:
        return f"Yes, {capitalize_name(person)} is {relation}."
    return f"No, {capitalize_name(person)} is not {relation}."


def _valid_person_pair(x, y):
    return x in KNOWN_NAMES and y in KNOWN_NAMES and is_safe_atom(x) and is_safe_atom(y)


def _property_yes_no(label, person, value, result):
    if result:
        return f"Yes, {capitalize_name(person)} is {label} {format_value(value)}."
    return f"No, {capitalize_name(person)} is not {label} {format_value(value)}."


def _looks_like_profile_request(text):
    return bool(re.search(r"\b(tell me about|about|profile|details|all about|information about)\b", text))


def _answer_city_list(text):
    city = None
    m = re.search(
        r"\b(?:who|which people|people|members|family members|show|list)\b.*\b(?:live|lives|living|from|in)\s+(\w+)\b",
        text,
    )
    if m:
        city = normalize_atom(m.group(1))
    else:
        m = re.search(r"\b(\w+)\s+(?:members|people|family)\b", text)
        if m:
            candidate = normalize_atom(m.group(1))
            if candidate in KNOWN_CITIES:
                city = candidate

    if not city:
        return None
    if city not in KNOWN_CITIES:
        return None

    results = _dedupe(query("lives_in", ["X", city]))
    if results:
        joined = ", ".join(format_value(name) for name in results)
        return f"Family members in {capitalize_name(city)}: {joined}."
    return f"No family members found in {capitalize_name(city)}."


def _answer_gender_list(text):
    if not re.search(r"\b(who|which|list|show)\b", text):
        return None

    for gender in ("male", "female"):
        if re.search(rf"\b{gender}\b", text):
            results = _unique_sorted(_dedupe(query(gender, ["X"])))
            if results:
                joined = ", ".join(format_value(name) for name in results)
                return f"{gender.capitalize()} family members: {joined}."
            return f"No {gender} family members found."

    return None


def _answer_family_member_list(text):
    if not re.search(r"\b(who|which|list|show|all|everyone)\b", text):
        return None

    if not re.search(r"\b(members?|people|everyone|all members|all people|family kb|family knowledge base|family members?)\b", text):
        return None

    if re.search(r"\b(male|female)\b", text):
        return None

    members = _dedupe(query("male", ["X"])) + _dedupe(query("female", ["X"]))
    members = _unique_sorted(members)
    if not members:
        return "I could not find any family members."
    return "All family members: " + ", ".join(format_value(member) for member in members) + "."


def _answer_all_members(text):
    if not re.search(r"\b(all family|all members|all people|everyone|list family|show family)\b", text):
        return None

    members = _dedupe(query("male", ["X"])) + _dedupe(query("female", ["X"]))
    members = _unique_sorted(members)
    if not members:
        return "I could not find any family members."
    return "All family members: " + ", ".join(format_value(member) for member in members) + "."


def _answer_same_group(text, names):
    if not names:
        return None
    relation = None
    if "same city" in text:
        relation = "same_city"
    elif "same occupation" in text or "same job" in text or "same profession" in text:
        relation = "same_occupation"
    elif "same generation" in text:
        relation = "same_generation"

    if not relation:
        return None
    results = _dedupe(query(relation, [names[0], "X"]))
    return format_response(relation, names[0], results)


def _answer_occupation_list(text):
    if extract_names(text):
        return None
    if not re.search(r"\b(who|list|show|which)\b", text):
        return None

    for token in words(text):
        occupation = _singular(token)
        if occupation in KNOWN_OCCUPATIONS:
            results = _dedupe(query("occupation", ["X", occupation]))
            if results:
                joined = ", ".join(format_value(name) for name in results)
                return f"Family members who are {occupation}s: {joined}."
            return f"No family members found with occupation {format_value(occupation)}."
    return None


def _answer_property(relation, person):
    results = _dedupe(query(relation, [person, "X"]))
    return format_response(relation, person, results)


def _answer_relationship(relation, person):
    results = _dedupe(query(relation, ["X", person]))
    return format_response(relation, person, results)


def _all_about(person):
    if person not in KNOWN_NAMES:
        return f"Sorry, I have no information about {capitalize_name(person)}."

    lines = [f"Here is what I know about {capitalize_name(person)}:"]

    def add(label, relation, args):
        results = _dedupe(query(relation, args))
        if results:
            lines.append(f"- {label}: {', '.join(format_value(item) for item in results)}")

    add("Father", "father", ["X", person])
    add("Mother", "mother", ["X", person])
    add("Spouse", "spouse", ["X", person])
    add("Children", "child", ["X", person])
    add("Siblings", "sibling", ["X", person])
    add("Grandparents", "grandparent", ["X", person])
    add("Date of birth", "dob", [person, "X"])
    add("Occupation", "occupation", [person, "X"])
    add("City", "lives_in", [person, "X"])
    add("Religion", "religion", [person, "X"])

    if len(lines) == 1:
        return f"Sorry, I have no information about {capitalize_name(person)}."
    return "\n".join(lines)


def _unique_sorted(values):
    return sorted(set(values), key=lambda value: format_value(value))


def _singular(word):
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def _fallback():
    return (
        "I can answer family knowledge-base questions best. Try asking things like:\n"
        "- who is Ali's father?\n"
        "- what is Ali's dob?\n"
        "- show siblings of Zain\n"
        "- list children of Ali\n"
        "- is Shakeel an ancestor of Zain?\n"
        "- who lives in Lahore?\n"
        "- tell me about Ali\n\n"
        "For general questions, no external AI or internet service is connected in this assignment version."
    )
