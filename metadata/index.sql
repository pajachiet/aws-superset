CREATE UNIQUE INDEX ON entreprise (identifiant);
CREATE UNIQUE INDEX ON declaration_remuneration (entreprise_identifiant, ligne_identifiant);
CREATE UNIQUE INDEX ON declaration_avantage (entreprise_identifiant, ligne_identifiant);
CREATE UNIQUE INDEX ON declaration_convention (entreprise_identifiant, ligne_identifiant);

CREATE INDEX ON declaration_remuneration (denomination_sociale);
CREATE INDEX ON declaration_avantage (denomination_sociale);
CREATE INDEX ON declaration_convention (denomination_sociale);


CREATE INDEX ON declaration_remuneration (@);
CREATE INDEX ON declaration_avantage ((upper(benef_nom) || ' ' || lower(benef_prenom)));
CREATE INDEX ON declaration_convention ((upper(benef_nom) || ' ' || lower(benef_prenom)));
