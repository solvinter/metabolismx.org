# Översikt: beräkningar och rapportlogik

Det här dokumentet beskriver vilka metabola beräkningar systemet ska stödja, hur de bör grupperas och hur de kan användas för att modifiera risknivåer från SCORE2/PREVENT utan att skapa en ny svart låda.

## Princip

Insulinresistens ska behandlas som en riskförstärkare, inte som en ensam diagnos eller ett ensamt poängsystem. Systemet ska identifiera en insulinresistent fenotyp genom flera samstämmiga signaler:

- högt midjemått
- triglycerider `>=1,7 mmol/L`
- lågt HDL
- förhöjd TG/HDL-kvot
- förhöjt fasteinsulin
- förhöjt HOMA-IR
- C-peptid förhöjt relativt glukos
- fasteglukos `5,6-6,9 mmol/L`
- blodtryck `>=130/80 mmHg`

Den praktiska slutsatsen ska formuleras som en delprofil eller risknivå, inte som en exakt ny CVD-procent.

## 1. HOMA-IR

HOMA-IR uppskattar insulinresistens från fasteinsulin och fasteglukos.

```text
HOMA-IR = fasteinsulin x fasteglukos / 22,5
```

Används när insulin anges i `mU/L` eller `uU/mL` och glukos i `mmol/L`.

Tolkning:

- högre värde talar för mer insulinresistens
- trösklar varierar med population, metod och klinisk kontext
- bör tolkas tillsammans med midja, TG, HDL, fasteglukos och C-peptid

## 2. QUICKI

QUICKI är en mer forskningspräglad men användbar kompletterande signal för insulinresistens.

```text
QUICKI = 1 / [log(insulin) + log(glukos)]
```

API-beslut:

- standardvarianten bör använda `log10`, fasteinsulin i `uU/mL` och fasteglukos i `mg/dL`
- om glukos kommer in som `mmol/L` ska den konverteras innan QUICKI beräknas
- lägre QUICKI talar för lägre insulinkänslighet

## 3. TyG-index

TyG-index fångar triglycerid-glukos-signalen och är praktiskt eftersom TG + glukos ofta speglar aterogen/metabol insulinresistens.

```text
TyG = ln[(triglycerider x fasteglukos) / 2]
```

API-beslut:

- standardvarianten bör använda triglycerider och glukos i `mg/dL`
- om indata är `mmol/L` konverteras triglycerider med `x 88,57` och glukos med `x 18,0182`
- TyG ska användas som kontinuerlig signal eller percentilbaserad flagga, inte som ensam diagnos

## 4. TG/HDL-kvot

TG/HDL är en enkel patientkommunikationsmarkör.

```text
TG/HDL = triglycerider / HDL
```

Tolkning:

- höga triglycerider + lågt HDL är en klassisk insulinresistent lipidbild
- signalen blir starkare tillsammans med förhöjt midjemått
- enhetsval måste vara konsekvent; europeisk bas bör vara `mmol/L`

## 5. Non-HDL-kolesterol

Non-HDL kostar inget extra och fångar aterogena ApoB-partiklar ungefärligt bättre än LDL ensamt vid insulinresistens.

```text
Non-HDL = total-kolesterol - HDL
```

Användning:

- alltid beräkna när total-kolesterol och HDL finns
- lyft fram när triglycerider är förhöjda eller LDL kan underskatta partikelbördan
- ApoB bör ersätta eller komplettera non-HDL om ApoB finns tillgängligt

## 6. Remnant cholesterol

Remnant-C är särskilt intressant vid höga triglycerider och metabol dysfunktion.

```text
Remnant-C = total-kolesterol - LDL - HDL
```

Användning:

- beräkna när total-kolesterol, LDL och HDL finns
- flagga datakvalitet om LDL är beräknat och triglycerider är höga
- använd som stöd för aterogen lipidprofil, inte som ensam behandlingsgrund

## 7. Total/HDL-kvot

Total/HDL-kvoten är bra för riskkommunikation.

```text
Total/HDL = total-kolesterol / HDL
```

Användning:

- pedagogisk sammanfattning av aterogen balans
- bör inte ersätta LDL, non-HDL eller ApoB

## 8. LDL/HDL-kvot

LDL/HDL är mindre elegant än ApoB, men användbar på basnivå.

```text
LDL/HDL = LDL / HDL
```

Användning:

- enkel kommunikationsmarkör
- sekundär till LDL, non-HDL och ApoB när dessa finns

## 9. Midja/längd-kvot

Waist-to-height ratio är en pedagogisk visceral adipositetsmarkör.

```text
Midja/längd = midja / längd
```

Budskap:

- "midjan bör helst vara under hälften av längden"
- kvot `>=0,5` kan flaggas som ökad visceral belastning
- ska bedömas tillsammans med BMI och könsspecifika midjegränser

## 10. Metabola syndromet

Systemet ska stödja metabola syndromet som en regelbaserad klassifikation.

Kriterier:

- högt midjemått
- triglycerider `>=1,7 mmol/L`
- lågt HDL
- blodtryck `>=130/85 mmHg` eller behandling
- fasteglukos `>=5,6 mmol/L`

API-beslut:

- stöd minst två konfigurationslägen: `IDF` och `JIS/NCEP`
- IDF-läge kräver centralt ökat midjemått plus minst två ytterligare kriterier
- JIS/NCEP-läge kan använda minst tre av fem kriterier
- insulinresistens är centralt biologiskt men inte ett obligatoriskt laboratoriekriterium

Föreslagna HDL-gränser i europeisk kontext:

| Kön | Lågt HDL |
| --- | ---: |
| Man | `<1,0 mmol/L` |
| Kvinna | `<1,3 mmol/L` |

Midjegränser ska ligga i konfiguration eftersom de varierar med definition och etnicitet.

## 11. Diabetes-/prediabetes-screening

Med fasteglukos kan systemet flagga:

| Fasteglukos | Klassifikation |
| ---: | --- |
| `<5,6 mmol/L` | Normal |
| `5,6-6,9 mmol/L` | Nedsatt fasteglukos/prediabetes |
| `>=7,0 mmol/L` | Diabetesmisstanke, kräver klinisk bekräftelse |

HbA1c och OGTT bör kunna läggas till i senare version. Systemet ska alltid formulera detta som screening eller misstanke, inte som definitiv diagnos.

## 12. Blodtrycksklassificering

Systemet ska separera blodtrycksklassifikation från optimalt riskmål.

Klassifikation:

| Nivå | Systoliskt | Diastoliskt |
| --- | ---: | ---: |
| Optimalt/lågt normalt | `<120` | `<70-80` beroende på vald guideline |
| Förhöjt | `120-139` | `70-89` |
| Hypertoni grad 1 | `140-159` | `90-99` |
| Hypertoni grad 2 | `160-179` | `100-109` |
| Hypertoni grad 3 | `>=180` | `>=110` |

För metabolt högriskpersoner är `140/90` för grovt som optimalt mål. Det är mer ett klassifikations- och behandlingsgolv än ett optimalt riskmål. Därför bör `>=130/80` kunna flaggas som metabol riskförstärkare även när formell hypertonidiagnos inte sätts.

## 397-rapportens fyra delprofiler

### A. Glukos-insulinprofil

Ingående data:

- fasteglukos
- fasteinsulin
- C-peptid
- HOMA-IR
- QUICKI
- HbA1c om tillgängligt

Fråga profilen ska besvara:

> Finns det en tidig eller tydlig insulinresistenssignal innan diabetesdiagnos?

### B. Aterogen lipidprofil

Ingående data:

- LDL
- HDL
- triglycerider
- non-HDL
- TG/HDL
- remnant-C
- ApoB om tillgängligt

Fråga profilen ska besvara:

> Finns en insulinresistent, ApoB-driven eller triglyceridrik lipidbild som förstärker CVD-risk?

### C. Visceral adipositetsprofil

Ingående data:

- midja
- BMI
- midja/längd
- köns- och etnicitetsspecifika midjegränser

Fråga profilen ska besvara:

> Finns en visceral adipositetsfenotyp som gör labbsignalerna mer sannolikt metabola?

### D. Klinisk riskprofil

Ingående data:

- ålder
- kön
- rökning
- blodtryck
- blodtrycksbehandling
- känd diabetes
- känd CVD
- SCORE2, SCORE2-OP eller PREVENT där lämpligt

Fråga profilen ska besvara:

> Hur hög är den validerade kliniska risken, och förstärks den av metabol fenotyp?

## Metabolic Risk Modifier

Basnivån kan skapa en intern modifieringsnivå, men inte en enda numerisk patientpoäng.

Starka signaler:

- midjemått över gräns
- triglycerider `>=1,7 mmol/L`
- lågt HDL
- TG/HDL förhöjt
- fasteinsulin förhöjt
- HOMA-IR förhöjt
- C-peptid förhöjt relativt glukos
- fasteglukos `5,6-6,9 mmol/L`
- blodtryck `>=130/80 mmHg`

Nivåer:

| Nivå | Regelidé |
| --- | --- |
| Låg | Få eller inga samstämmiga metabola signaler |
| Måttlig | Flera milda signaler eller en tydlig signal |
| Tydlig | Tydlig insulinresistent fenotyp eller metabola syndromet |
| Mycket hög | Tydlig IR plus flera kliniska riskfaktorer, diabetesmisstanke eller mycket ogynnsam lipid-/BT-profil |

## Rimlig lipidstrategi

| Modifiernivå | Strategi |
| --- | --- |
| Låg | Vanligt LDL-mål enligt ålder, riktlinje och SCORE2 |
| Måttlig | Behandla som riskförstärkare; sikta lägre än standard om totalbilden talar för det |
| Tydlig IR/metabola syndromet | Överväg LDL `<2,6 mmol/L` eller `<1,8 mmol/L` beroende på totalrisk |
| Mycket hög belastning plus flera riskfaktorer | Argument för diabetikernära lipidmål även före diagnos |

Kärnargument:

> Insulinresistens är en tillräckligt stark riskmodifierare för att motivera lägre LDL-mål innan diabetes uppstår, men systemet ska visa vilka mätbara signaler som ligger bakom.

Exempel:

```text
TG/HDL = 2,3
midja = 12 cm över cut-off
HOMA-IR = hög
```

Tolkning:

```text
Definierad insulinresistent fenotyp
=> metabol riskmodifiering
=> justerat LDL-mål kan övervägas
```

## Scenario-modellering

Systemet bör visa riskreduktion via mediatorer, inte via ett direkt antagande om insulinresistens.

Insulinresistens påverkar ofta:

- triglycerider upp
- HDL ned
- blodtryck upp
- glukos upp
- ApoB/non-HDL upp indirekt

Modellering:

1. Identifiera insulinresistent fenotyp.
2. Simulera förbättringar i TG, HDL, blodtryck och glukos.
3. Räkna om validerad riskmodell där variablerna stöds.
4. Presentera skillnaden som scenario.

Exempel:

| Scenario | TG | HDL | SBP | Risk |
| --- | ---: | ---: | ---: | ---: |
| Nu | 2,2 | 0,9 | 138 | 12% |
| Förbättrad metabol profil | 1,2 | 1,3 | 122 | 7% |

Text:

> Denna förändring motsvarar cirka 5 procentenheters lägre beräknad 10-årsrisk i scenariot.

## Kort slutsats

- Det finns inte LDL-liknande data där insulinresistens direkt kan översättas till exakt riskreduktion i procent.
- Det finns starkt stöd för att insulinresistens och dess fenotyp är kopplad till högre kardiometabol risk.
- Systemet bör därför modellera risk via förändring i downstream-markörer som redan ingår i etablerade riskmodeller eller kliniska mål.
- Det praktiska värdet är att göra "patienten är metabolt belastad" mätbart, spårbart och kommunicerbart.
