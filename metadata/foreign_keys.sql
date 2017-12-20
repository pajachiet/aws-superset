ALTER TABLE declaration_remuneration ADD CONSTRAINT declaration_remuneration_entreprise_fk FOREIGN KEY (entreprise_identifiant) REFERENCES entreprise (identifiant) MATCH FULL;
ALTER TABLE declaration_convention ADD CONSTRAINT declaration_convention_entreprise_fk FOREIGN KEY (entreprise_identifiant) REFERENCES entreprise (identifiant) MATCH FULL;
ALTER TABLE declaration_avantage ADD CONSTRAINT declaration_avantage_entreprise_fk FOREIGN KEY (entreprise_identifiant) REFERENCES entreprise (identifiant) MATCH FULL;
