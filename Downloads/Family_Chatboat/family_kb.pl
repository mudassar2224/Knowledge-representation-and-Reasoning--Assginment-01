% =========================================================
% FAMILY KNOWLEDGE BASE - PYTHOLOG COMPATIBLE
% =========================================================
% Pytholog has limited support for normal Prolog operators. This file avoids
% quoted atoms, \+, ;, !, and \= so every rule can be loaded safely.

% =========================================================
% FACT TYPE 1: GENDER FACTS
% =========================================================

male(ali).
male(asad).
male(shakeel).
male(zain).
male(hamza).
male(usman).
male(bilal).
male(tariq).

female(alia).
female(shakeela).
female(zaini).
female(laiba).
female(sana).
female(nadia).
female(rukhsana).
female(hina).

% =========================================================
% FACT TYPE 2: PARENT FACTS
% parent(Parent, Child)
% =========================================================

parent(ali, zain).
parent(ali, zaini).
parent(alia, zain).
parent(alia, zaini).

parent(shakeel, ali).
parent(shakeela, ali).
parent(shakeel, asad).
parent(shakeela, asad).
parent(shakeel, nadia).
parent(shakeela, nadia).

parent(asad, laiba).
parent(sana, laiba).
parent(asad, bilal).
parent(sana, bilal).

parent(hamza, sana).
parent(rukhsana, sana).
parent(hamza, usman).
parent(rukhsana, usman).

parent(tariq, alia).
parent(hina, alia).
parent(tariq, usman).

% =========================================================
% FACT TYPE 3: MARRIED FACTS
% married(Husband, Wife)
% =========================================================

married(ali, alia).
married(shakeel, shakeela).
married(asad, sana).
married(hamza, rukhsana).
married(tariq, hina).

% =========================================================
% FACT TYPE 4: DATE OF BIRTH FACTS
% Dates are atoms so Pytholog returns them as values, not just "Yes".
% =========================================================

dob(ali, d2000_05_12).
dob(asad, d1998_09_21).
dob(shakeel, d1970_02_10).
dob(shakeela, d1972_07_15).
dob(alia, d2001_03_05).
dob(zain, d2022_01_10).
dob(zaini, d2023_06_20).
dob(laiba, d2019_11_03).
dob(bilal, d2021_04_17).
dob(sana, d1999_08_30).
dob(hamza, d1968_12_01).
dob(rukhsana, d1970_05_22).
dob(nadia, d2002_09_14).
dob(usman, d1995_03_28).
dob(tariq, d1965_11_09).
dob(hina, d1968_04_03).

% =========================================================
% FACT TYPE 5: OCCUPATION FACTS
% =========================================================

occupation(shakeel, doctor).
occupation(shakeela, teacher).
occupation(ali, engineer).
occupation(alia, nurse).
occupation(asad, lawyer).
occupation(sana, accountant).
occupation(hamza, businessman).
occupation(tariq, professor).
occupation(hina, principal).
occupation(usman, pilot).
occupation(nadia, student).

% =========================================================
% FACT TYPE 6: CITY / LOCATION FACTS
% =========================================================

lives_in(shakeel, lahore).
lives_in(shakeela, lahore).
lives_in(ali, lahore).
lives_in(alia, lahore).
lives_in(zain, lahore).
lives_in(zaini, lahore).
lives_in(asad, karachi).
lives_in(sana, karachi).
lives_in(laiba, karachi).
lives_in(bilal, karachi).
lives_in(hamza, islamabad).
lives_in(rukhsana, islamabad).
lives_in(usman, islamabad).
lives_in(tariq, peshawar).
lives_in(hina, peshawar).
lives_in(nadia, lahore).

% =========================================================
% FACT TYPE 7: RELIGION FACTS
% =========================================================

religion(ali, islam).
religion(alia, islam).
religion(shakeel, islam).
religion(shakeela, islam).
religion(asad, islam).
religion(sana, islam).
religion(hamza, islam).
religion(rukhsana, islam).
religion(tariq, islam).
religion(hina, islam).

% =========================================================
% PYTHOLOG-SAFE INEQUALITY FACTS
% =========================================================
% different(X, Y) replaces unsupported X \= Y in all rules.

different(ali, asad).
different(ali, shakeel).
different(ali, zain).
different(ali, hamza).
different(ali, usman).
different(ali, bilal).
different(ali, tariq).
different(ali, alia).
different(ali, shakeela).
different(ali, zaini).
different(ali, laiba).
different(ali, sana).
different(ali, nadia).
different(ali, rukhsana).
different(ali, hina).
different(asad, ali).
different(asad, shakeel).
different(asad, zain).
different(asad, hamza).
different(asad, usman).
different(asad, bilal).
different(asad, tariq).
different(asad, alia).
different(asad, shakeela).
different(asad, zaini).
different(asad, laiba).
different(asad, sana).
different(asad, nadia).
different(asad, rukhsana).
different(asad, hina).
different(shakeel, ali).
different(shakeel, asad).
different(shakeel, zain).
different(shakeel, hamza).
different(shakeel, usman).
different(shakeel, bilal).
different(shakeel, tariq).
different(shakeel, alia).
different(shakeel, shakeela).
different(shakeel, zaini).
different(shakeel, laiba).
different(shakeel, sana).
different(shakeel, nadia).
different(shakeel, rukhsana).
different(shakeel, hina).
different(zain, ali).
different(zain, asad).
different(zain, shakeel).
different(zain, hamza).
different(zain, usman).
different(zain, bilal).
different(zain, tariq).
different(zain, alia).
different(zain, shakeela).
different(zain, zaini).
different(zain, laiba).
different(zain, sana).
different(zain, nadia).
different(zain, rukhsana).
different(zain, hina).
different(hamza, ali).
different(hamza, asad).
different(hamza, shakeel).
different(hamza, zain).
different(hamza, usman).
different(hamza, bilal).
different(hamza, tariq).
different(hamza, alia).
different(hamza, shakeela).
different(hamza, zaini).
different(hamza, laiba).
different(hamza, sana).
different(hamza, nadia).
different(hamza, rukhsana).
different(hamza, hina).
different(usman, ali).
different(usman, asad).
different(usman, shakeel).
different(usman, zain).
different(usman, hamza).
different(usman, bilal).
different(usman, tariq).
different(usman, alia).
different(usman, shakeela).
different(usman, zaini).
different(usman, laiba).
different(usman, sana).
different(usman, nadia).
different(usman, rukhsana).
different(usman, hina).
different(bilal, ali).
different(bilal, asad).
different(bilal, shakeel).
different(bilal, zain).
different(bilal, hamza).
different(bilal, usman).
different(bilal, tariq).
different(bilal, alia).
different(bilal, shakeela).
different(bilal, zaini).
different(bilal, laiba).
different(bilal, sana).
different(bilal, nadia).
different(bilal, rukhsana).
different(bilal, hina).
different(tariq, ali).
different(tariq, asad).
different(tariq, shakeel).
different(tariq, zain).
different(tariq, hamza).
different(tariq, usman).
different(tariq, bilal).
different(tariq, alia).
different(tariq, shakeela).
different(tariq, zaini).
different(tariq, laiba).
different(tariq, sana).
different(tariq, nadia).
different(tariq, rukhsana).
different(tariq, hina).
different(alia, ali).
different(alia, asad).
different(alia, shakeel).
different(alia, zain).
different(alia, hamza).
different(alia, usman).
different(alia, bilal).
different(alia, tariq).
different(alia, shakeela).
different(alia, zaini).
different(alia, laiba).
different(alia, sana).
different(alia, nadia).
different(alia, rukhsana).
different(alia, hina).
different(shakeela, ali).
different(shakeela, asad).
different(shakeela, shakeel).
different(shakeela, zain).
different(shakeela, hamza).
different(shakeela, usman).
different(shakeela, bilal).
different(shakeela, tariq).
different(shakeela, alia).
different(shakeela, zaini).
different(shakeela, laiba).
different(shakeela, sana).
different(shakeela, nadia).
different(shakeela, rukhsana).
different(shakeela, hina).
different(zaini, ali).
different(zaini, asad).
different(zaini, shakeel).
different(zaini, zain).
different(zaini, hamza).
different(zaini, usman).
different(zaini, bilal).
different(zaini, tariq).
different(zaini, alia).
different(zaini, shakeela).
different(zaini, laiba).
different(zaini, sana).
different(zaini, nadia).
different(zaini, rukhsana).
different(zaini, hina).
different(laiba, ali).
different(laiba, asad).
different(laiba, shakeel).
different(laiba, zain).
different(laiba, hamza).
different(laiba, usman).
different(laiba, bilal).
different(laiba, tariq).
different(laiba, alia).
different(laiba, shakeela).
different(laiba, zaini).
different(laiba, sana).
different(laiba, nadia).
different(laiba, rukhsana).
different(laiba, hina).
different(sana, ali).
different(sana, asad).
different(sana, shakeel).
different(sana, zain).
different(sana, hamza).
different(sana, usman).
different(sana, bilal).
different(sana, tariq).
different(sana, alia).
different(sana, shakeela).
different(sana, zaini).
different(sana, laiba).
different(sana, nadia).
different(sana, rukhsana).
different(sana, hina).
different(nadia, ali).
different(nadia, asad).
different(nadia, shakeel).
different(nadia, zain).
different(nadia, hamza).
different(nadia, usman).
different(nadia, bilal).
different(nadia, tariq).
different(nadia, alia).
different(nadia, shakeela).
different(nadia, zaini).
different(nadia, laiba).
different(nadia, sana).
different(nadia, rukhsana).
different(nadia, hina).
different(rukhsana, ali).
different(rukhsana, asad).
different(rukhsana, shakeel).
different(rukhsana, zain).
different(rukhsana, hamza).
different(rukhsana, usman).
different(rukhsana, bilal).
different(rukhsana, tariq).
different(rukhsana, alia).
different(rukhsana, shakeela).
different(rukhsana, zaini).
different(rukhsana, laiba).
different(rukhsana, sana).
different(rukhsana, nadia).
different(rukhsana, hina).
different(hina, ali).
different(hina, asad).
different(hina, shakeel).
different(hina, zain).
different(hina, hamza).
different(hina, usman).
different(hina, bilal).
different(hina, tariq).
different(hina, alia).
different(hina, shakeela).
different(hina, zaini).
different(hina, laiba).
different(hina, sana).
different(hina, nadia).
different(hina, rukhsana).

% =========================================================
% BASIC RELATION RULES
% =========================================================

father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).
son(X, Y) :- male(X), parent(Y, X).
daughter(X, Y) :- female(X), parent(Y, X).
child(X, Y) :- parent(Y, X).
husband(X, Y) :- married(X, Y).
wife(X, Y) :- married(Y, X).

% =========================================================
% SIBLING RULES
% =========================================================

sibling(X, Y) :- parent(Z, X), parent(Z, Y), different(X, Y).
brother(X, Y) :- sibling(X, Y), male(X).
sister(X, Y) :- sibling(X, Y), female(X).

% =========================================================
% GRANDPARENT RULES
% =========================================================

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- father(X, Z), parent(Z, Y).
grandmother(X, Y) :- mother(X, Z), parent(Z, Y).
grandchild(X, Y) :- grandparent(Y, X).
grandson(X, Y) :- grandchild(X, Y), male(X).
granddaughter(X, Y) :- grandchild(X, Y), female(X).

% =========================================================
% DADA / DADI / NANA / NANI (CULTURAL GRANDPARENT TERMS)
% =========================================================

dada(X, Y) :- father(F, Y), father(X, F).
dadi(X, Y) :- father(F, Y), mother(X, F).
nana(X, Y) :- mother(M, Y), father(X, M).
nani(X, Y) :- mother(M, Y), mother(X, M).

% =========================================================
% EXTENDED FAMILY RULES
% =========================================================

uncle(X, Y) :- brother(X, Z), parent(Z, Y).
aunt(X, Y) :- sister(X, Z), parent(Z, Y).
cousin(X, Y) :- parent(A, X), parent(B, Y), sibling(A, B), different(X, Y).
nephew(X, Y) :- male(X), sibling(Z, Y), parent(Z, X).
niece(X, Y) :- female(X), sibling(Z, Y), parent(Z, X).

% =========================================================
% EASTERN / URDU RELATION RULES
% =========================================================

chacha(X, Y) :- father(F, Y), brother(X, F).
phoophi(X, Y) :- father(F, Y), sister(X, F).
maamu(X, Y) :- mother(M, Y), brother(X, M).
khala(X, Y) :- mother(M, Y), sister(X, M).
chachi(X, Y) :- chacha(C, Y), married(C, X).
phuppa(X, Y) :- phoophi(P, Y), married(X, P).
maami(X, Y) :- maamu(M, Y), married(M, X).
khalu(X, Y) :- khala(K, Y), married(X, K).

% =========================================================
% IN-LAW RULES (split into separate rules - no semicolon)
% =========================================================

father_in_law(X, Y) :- married(Y, S), father(X, S).
father_in_law(X, Y) :- married(S, Y), father(X, S).
mother_in_law(X, Y) :- married(Y, S), mother(X, S).
mother_in_law(X, Y) :- married(S, Y), mother(X, S).
brother_in_law(X, Y) :- married(Y, S), brother(X, S).
brother_in_law(X, Y) :- married(S, Y), brother(X, S).
sister_in_law(X, Y) :- married(Y, S), sister(X, S).
sister_in_law(X, Y) :- married(S, Y), sister(X, S).
son_in_law(X, Y) :- daughter(D, Y), married(X, D).
son_in_law(X, Y) :- daughter(D, Y), married(D, X).
daughter_in_law(X, Y) :- son(S, Y), married(S, X).
daughter_in_law(X, Y) :- son(S, Y), married(X, S).

% =========================================================
% ANCESTOR / DESCENDANT RECURSION
% =========================================================

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
descendant(X, Y) :- ancestor(Y, X).

% =========================================================
% SAME CITY / SAME OCCUPATION / GENERATION RULES
% =========================================================

same_city(X, Y) :- lives_in(X, C), lives_in(Y, C), different(X, Y).
same_occupation(X, Y) :- occupation(X, O), occupation(Y, O), different(X, Y).
same_generation(X, Y) :- grandparent(G, X), grandparent(G, Y), different(X, Y).
same_generation(X, Y) :- parent(P, X), parent(P, Y), different(X, Y).

% =========================================================
% BLOOD RELATIVE / FAMILY MEMBER RULES
% =========================================================

blood_relative(X, Y) :- ancestor(X, Y).
blood_relative(X, Y) :- ancestor(Y, X).
blood_relative(X, Y) :- sibling(X, Y).
blood_relative(X, Y) :- cousin(X, Y).
blood_relative(X, Y) :- ancestor(Z, X), ancestor(Z, Y), different(X, Y).
family_member(X, Y) :- parent(X, Y).
family_member(X, Y) :- parent(Y, X).
family_member(X, Y) :- sibling(X, Y).

% =========================================================
% SPOUSE RULES
% =========================================================

spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).
