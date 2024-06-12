import os
import json
from google.cloud import secretmanager
import gcloud_config_helper
from typing import Optional, Dict


class Tilgangskontroll:
    """
    En klasse brukt til å håndtere tilgangskontroll.

    ...

    Metoder
    -------
    sjekk_om_kjoerelokasjon_er_lokal():
        Sjekker om kjøreløkasjonen er lokal.
    hent_datamarkedsplassen_team_token(dev_env: str) -> str:
        Henter team token for datamarkedsplassen.
    hent_prosjektid_amplitude() -> str:
        Henter prosjektid for amplitude.
    """

    def __init__(self):
        """
        Konstruktør for Tilgangskontroll klassen.
        """
        self.brukernavn = self._hent_brukernavn()
        self._knada_hemeligheter = self._hent_hemmeligheter("KNADA")
        self.prosjektnavn = self._hent_prosjektnavn()
        self.gcp_hemmeligheter = self._hent_hemmeligheter("GCP")

    def sjekk_om_kjoerelokasjon_er_lokal(self) -> bool:
        """
        Sjekker om kjøreløkasjonen er lokal.

        Returns
        -------
        bool
            True hvis kjøreløkasjonen er lokal, False ellers.
        """
        return "LOGNAME" in os.environ   


    def _hent_brukernavn(self) -> str:
        if self.sjekk_om_kjoerelokasjon_er_lokal():
            brukernavn = (
                gcloud_config_helper.default()[0]
                .properties["core"]["account"]
                .split("@")[0]
                .replace(".", "_")
                )
        elif "JUPYTERHUB_USER" in os.environ:
            brukernavn = os.environ["JUPYTERHUB_USER"].split("@")[0].replace(".", "_")
        else:
            brukernavn = "airflow"
        return brukernavn

    def _hent_prosjektnavn(self) -> str:
        """
        Henter prosjektnavnet.

        Returns
        -------
        str
            Prosjektnavnet.
        """
        if self.sjekk_om_kjoerelokasjon_er_lokal():
            prosjektnavn = input("Sett prosjektnavnet fra GCP: ")
        else:
            prosjektnavn = self._hent_knada_prosjektnavn()
        return prosjektnavn
    

    def _hent_knada_prosjektnavn(self):
        """
        Henter prosjektnavnet fra KNADA hemmeligheter.

        Returns
        -------
        str
            Prosjektnavnet.
        """
        prosjektnavn = self._knada_hemeligheter["GCP_PAW_PROD"].get("project_id")
        return prosjektnavn


    def _hent_hemmeligheter(self, kilde: str) -> Optional[Dict[str, str]]:
        """
        Henter hemmeligheter fra en gitt kilde.

        Parameters
        ----------
        kilde : str
            Kilden til hemmelighetene.

        Returns
        -------
        dict
            Hemmelighetene.
        """
        if kilde == "GCP":
            lokasjon_hemmeligheter = f"projects/{self.prosjektnavn}/secrets/knorten_{self.brukernavn}/versions/latest"
        elif kilde == "KNADA" and "KNADA_TEAM_SECRET" in os.environ:
            lokasjon_hemmeligheter = f"{os.environ['KNADA_TEAM_SECRET']}/versions/latest"
        else:
            return
        secrets_instans = secretmanager.SecretManagerServiceClient(
                            ).access_secret_version(name=lokasjon_hemmeligheter)
        hemmeligheter = json.loads(secrets_instans.payload.data.decode("UTF-8"))
        return hemmeligheter

    def hent_datamarkedsplassen_team_token(self, dev_env: str) -> str:
        """
        Henter team token for datamarkedsplassen.

        Parameters
        ----------
        dev_env : str
            Utviklingsmiljøet.

        Returns
        -------
        str
            Team token.
        """
        if dev_env == "PROD":
            env = "team_token"
        elif dev_env == "DEV":
            env = "team_token_dev"
        team_token = self.gcp_hemmeligheter[env]
        return team_token