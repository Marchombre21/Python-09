# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    alien_contact.py                                   :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/02/03 07:35:37 by bfitte            #+#    #+#             #
#    Updated: 2026/02/03 07:35:38 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

try:
    import sys
    from datetime import datetime
    from typing_extensions import Self
    from enum import Enum
    from pydantic import BaseModel, Field, ValidationError, model_validator
except (ImportError, ModuleNotFoundError):
    print("Pydantic librairy is missing.\nMake sure you are in a virtual"
          " environment, then download it by typing the command:")
    print("pip install pydantic")
    sys.exit(1)


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field("", max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_values(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError(f"{self.contact_id} isn't a valid id.")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError(f"{self.contact_type.value} contact must be"
                             " verified")
        if self.contact_type == ContactType.TELEPATHIC and\
                self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3"
                             " witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include received"
                             " messages")
        return self


def main():
    print("\nAlien Contact Log Validation")
    print("======================================")
    contact_reports: list = [

        # A valid contact
        {
            "contact_id": "AC_001",
            "timestamp": "1992-10-10",
            "location": "Uranus",
            "contact_type": ContactType.PHYSICAL,
            "signal_strength": 8.2,
            "duration_minutes": 596,
            "witness_count": 60,
            "message_received": "Coucou",
            "is_verified": True,
        },

        # An invalid contact because of invalid types or fields and ONE error
        # from model_validator which will be unseen
        {
            "contact_id": "truc_001",
            "timestamp": "1992/10/10",
            "location": "Ur",
            "contact_type": "Olfactif",
            "signal_strength": 102.5,
            "duration_minutes": "596",
            "witness_count": 103,
            "message_received": None,
            "is_verified": None,
        },

        # An invalid contact because of model_validator. Both type and fields
        # are good
        {
            "contact_id": "AC_002",
            "timestamp": "1992-10-10",
            "location": "Uranus",
            "contact_type": ContactType.PHYSICAL,
            "signal_strength": 8.2,
            "duration_minutes": 596,
            "witness_count": 2,
            "message_received": "",
            "is_verified": False,
        }
    ]
    for contact in contact_reports:
        try:
            model = AlienContact(**contact)
            print("\nValid contact report:")
            print(f"ID: {model.contact_id}")
            print(f"Type: {model.contact_type.value}")
            print(f"Location: {model.location}")
            print(f"Signal: {model.signal_strength}/10")
            print(f"Duration: {model.duration_minutes} minutes")
            print(f"Witnesses: {model.witness_count}")
            print(f"Message: {model.message_received}")
            print()
            print("="*60)
        except (ValidationError, Exception) as e:
            print("Expected validation error:")
            for error in e.errors():

                # When the raised error come from model_validator there isn't
                # error["loc"] so I have to do like this
                loc: str = "" if not error["loc"] else f"{error['loc'][0]}: "
                print(f"{loc}{error['msg']}")
            print("="*60)


if __name__ == "__main__":
    main()
