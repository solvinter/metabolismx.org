# Metabolic Modifier System

API för beräkning av metabolt status som modulerar risknivåer beräknade ur SCORE2.

Syftet är att göra den metabola riskförstärkaren explicit. Systemet ska inte ersätta SCORE2 eller annan validerad riskmotor. Det ska lägga ett transparent metabolt lager ovanpå etablerad riskberäkning och visa varför en patient kan behöva ett lägre behandlingsmål än den rena SCORE2-procenten antyder.

## Grundidé

Baslagret gör deterministiska beräkningar i Python. Det ska vara läsbart, testbart och pedagogiskt:

- normalisera enheter
- beräkna metabola index
- klassificera delprofiler
- skapa ett strukturerat JSON-underlag
- hålla formler, trösklar och antaganden versionerade

Nästa lager är ett API som exponerar dessa beräkningar till ett gränssnitt. Det sista lagret är ett AI-stöd som tolkar det strukturerade underlaget och genererar en kliniskt läsbar 397-rapport.

AI-lagret ska inte hitta på egna riskprocent. Det ska läsa fält från Python/API-lagret, beskriva osäkerhet, ange vilka data som saknas och skilja mellan uppmätta värden, beräknade värden och infererade riskmönster.

## Planerade outputområden

- Prediabetes-/diabetesrisk
- Insulinresistensprofil
- Metabola syndromet
- Aterogen dyslipidemi
- Blodtrycksrisk och prehypertoni/förhöjt blodtryck
- 10-årig CVD-risk via SCORE2, SCORE2-OP eller PREVENT där det är lämpligt
- Metabol riskmodifiering av LDL-mål och uppföljningsnivå
- Scenario-modellering av riskreduktion via förbättrade mediatorer

## Viktig designprincip

Systemet ska inte ge en enda totalpoäng. Rapporten ska byggas av fyra delprofiler:

| Profil | Innehåll |
| --- | --- |
| A. Glukos-insulinprofil | Fasteglukos, fasteinsulin, C-peptid, HOMA-IR, QUICKI |
| B. Aterogen lipidprofil | LDL, HDL, triglycerider, non-HDL, TG/HDL, remnant-C |
| C. Visceral adipositetsprofil | Midja, BMI, midja/längd |
| D. Klinisk riskprofil | Blodtryck, rökning, ålder, kön, SCORE2/PREVENT där lämpligt |

En sammanfattande nivå kan finnas i rapporten, men den ska vara en slutsats från delprofilerna och inte en egen svart låda.

## 397-rapportens tre utfall

| Nivå | Tolkning | Praktisk konsekvens |
| --- | --- | --- |
| 1. Låg risk | Ingen tydlig metabol riskförstärkning | Livsstil, normal uppföljning |
| 2. Metabol risk, preklinisk | Tidig insulinresistens eller metabol belastning sannolik | Stark livsstilsintervention och planerad uppföljning |
| 3. Hög metabol risk | Tydlig insulinresistent fenotyp, metabola syndromet eller flera starka signaler | Klinisk utredning bör övervägas; läkemedelsdiskussion kan bli relevant |

## Riskmodifiering av LDL-mål

Detta lager ska kunna föreslå en mer ambitiös LDL-strategi när den metabola fenotypen talar för högre livstidsrisk än SCORE2 ensamt fångar.

| Metabol fenotyp | Rimlig LDL-tolkning i systemet |
| --- | --- |
| Metabolt frisk | Vanligt LDL-mål enligt ålder, totalrisk och SCORE2 |
| Mild insulinresistens eller metabol risk | Behandla som riskförstärkare; överväg lägre mål, ofta omkring `<2,6 mmol/L` |
| Tydlig insulinresistens eller metabola syndromet | Överväg `<2,6 mmol/L` eller `<1,8 mmol/L` beroende på totalrisk |
| Diabetes eller mycket hög samlad belastning | Diabetikernära mål kan vara rimliga, ofta omkring `<1,4-1,8 mmol/L` beroende på riktlinje och kontext |

Detta är en beslutslogik för riskkommunikation och kliniskt resonemang. Det ska inte presenteras som en fristående behandlingsrekommendation utan kontext.

## Mediator-baserad riskreduktion

Det finns inte ett enkelt LDL-liknande samband där "HOMA-IR ned X ger CVD-risk ned Y". Därför ska systemet modellera risk via downstream-markörer:

1. Identifiera insulinresistent fenotyp.
2. Simulera förbättringar i triglycerider, HDL, blodtryck och glukos.
3. Skicka nuvarande och förbättrat scenario till SCORE2/PREVENT där modellen stödjer dessa variabler.
4. Visa skillnaden som scenario, inte som bevisad individuell prognos.

Exempel:

| Scenario | TG | HDL | SBP | Beräknad risk |
| --- | ---: | ---: | ---: | ---: |
| Nuvarande profil | 2,2 | 0,9 | 138 | 12% |
| Förbättrad metabol profil | 1,2 | 1,3 | 122 | 7% |

Rapporttext: "Denna förändring motsvarar cirka 5 procentenheters lägre beräknad 10-årsrisk i scenariot."

## Datakontrakt, grovt

Input bör delas upp i:

- demografi: ålder, kön, land/riskregion, etnicitet där relevant
- riskfaktorer: rökning, blodtrycksbehandling, lipidsänkande behandling, känd CVD, känd diabetes
- antropometri: längd, vikt, midja
- blodtryck: systoliskt och diastoliskt, mätmetod
- lipider: total-kolesterol, LDL, HDL, triglycerider, ApoB om tillgängligt
- glukos-insulin: fasteglukos, fasteinsulin, C-peptid, HbA1c om tillgängligt

Output bör vara maskinläsbar JSON med:

- beräknade värden
- flaggor
- delprofilnivåer
- datakvalitet och saknade fält
- riskmotorresultat
- rapportunderlag för AI-lagret

## Repo-strategi

Starta som mapp i `metabolismx.org` medan begrepp, formler och rapportstruktur utvecklas nära övrigt material.

Bryt ut till separat repo när något av detta blir sant:

- API:t ska versioneras och testas självständigt
- Python-paketet ska installeras eller återanvändas i flera projekt
- det behövs CI, release-taggar eller klinisk valideringshistorik
- gränssnittet ska konsumera API:t som en fristående tjänst
- externa användare eller samarbeten ska kunna bidra utan att få hela webbplatsrepo:t

Tills dess är en mapp i huvudrepo:t pragmatisk och enklast att iterera på.

## Dokument

- [OVERSIKT.md](./OVERSIKT.md) beskriver vad som ska beräknas och hur rapporten bör modelleras.
- [python/README.md](./python/README.md) beskriver den planerade Python-strukturen.

## Referenser att validera mot

- SCORE2: https://academic.oup.com/eurheartj/article/42/25/2439/6297709
- SCORE2-OP: https://pmc.ncbi.nlm.nih.gov/articles/PMC8248997/
- ADA diabetesdiagnostik: https://diabetes.org/about-diabetes/diagnosis
- IDF metabola syndromet: https://idf.org/about-diabetes/resources/idf-consensus-worldwide-definition-of-the-metabolic-syndrome/
- ESC 2024 blodtryck: https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2024/09/05/14/11/2024-esc-guidelines-for-bp-esc-2024
- Surrogatmått för insulinresistens: https://pmc.ncbi.nlm.nih.gov/articles/PMC11475114/
