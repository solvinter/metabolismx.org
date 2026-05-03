# QUICKI

Syfte: Beskriva QUICKI som ett invers modellbaserat mått på insulinkänslighet i MetabolismX.

Status: draft

## Fysiologi

QUICKI står för Quantitative Insulin Sensitivity Check Index. Det beräknas från fasteinsulin och fasteglukos med logaritmisk transformation.

Formeln använder insulin i µU/mL och glukos i mg/dL:

```text
QUICKI = 1 / [log(insulin) + log(glukos)]
```

Högre QUICKI talar generellt för bättre insulinkänslighet. Lägre QUICKI talar för mer insulinresistens.

## Tolkning

QUICKI är ett modellbaserat index, inte en direkt clamp-mätning. Det ska därför inte tolkas som en diagnos.

QUICKI kan fungera som ett komplement till HOMA-IR. Där HOMA-IR stiger vid högre insulin-glukosbelastning sjunker QUICKI när insulinkänsligheten är lägre. De beskriver alltså samma område från olika håll.

Eftersom QUICKI bygger på fasteinsulin påverkas det av samma begränsningar: provtagningsstandardisering, biologisk variation, analysmetod och fastande status.

## Relaterade markörer

### HOMA-IR

HOMA-IR och QUICKI bör läsas tillsammans. Ett högt HOMA-IR och lågt QUICKI ger en samstämmig insulinresistenssignal.

### Fasteinsulin och fasteglukos

QUICKI kan inte förstås utan de två ingående värdena. Ett normalt glukosvärde med högt insulin kan sänka QUICKI och visa kompensatorisk belastning.

### C-peptid

C-peptid ger information om endogen insulinproduktion och kan hjälpa till att förstå om insulinmönstret är kompensatoriskt.

### TyG, TG/HDL och midja

QUICKI blir mer relevant när det stämmer överens med lipid- och antropometriska signaler som TyG, TG/HDL-kvot och midjemått.

## MetabolismX-princip

QUICKI är ett invers mått på insulinresistens: högre värde talar för bättre insulinkänslighet.

## Klinisk implikation

QUICKI används i MetabolismX som kompletterande insulinresistenssignal. Det ersätter inte HOMA-IR, klinisk bedömning eller validerade diagnostiska metoder och ger ingen behandlingsrekommendation.

## Referenser att validera

- Katz et al., 2000: ursprunglig QUICKI-validering.
- Studier om QUICKI jämfört med clamp-mätningar.
- Studier om QUICKI, HOMA-IR och fasteinsulin i metabol riskbedömning.
