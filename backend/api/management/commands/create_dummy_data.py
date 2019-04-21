#  rlcapp - record and organization management software for refugee law clinics
#  Copyright (C) 2019  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

import random

from django.core.management.base import BaseCommand

from backend.api import models as apimodels
from backend.api.management.commands._fixtures import AddMethods
from backend.recordmanagement import models
from backend.static import permissions


class Command(BaseCommand):
    help = 'populates database for deployment environment'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        rlc = apimodels.Rlc(name='Dummy RLC', note='this is a dummy rlc, just for showing how the system works')
        rlc.save()
        users = self.get_and_create_users(rlc)
        main_user = self.get_and_create_dummy_user(rlc)
        self.create_groups(rlc, main_user, users)
        clients = self.get_and_create_clients()
        consultant_group = apimodels.Group.objects.filter(name='Berater', from_rlc=rlc).first()
        records = self.get_and_create_records(clients, list(consultant_group.group_members.all()), rlc)

    def get_and_create_dummy_user(self, rlc):
        user = apimodels.UserProfile(name='Mr Dummy', email='dummy@rlcm.de', phone_number='01666666666',
                                  street='Dummyweg 12', city='Dummycity', postal_code='00000', rlc=rlc)
        user.birthday = AddMethods.generate_date((1995, 1, 1))
        user.set_password('qwe123')
        user.save()
        return user

    def get_and_create_users(self, rlc):
        users = [
            (
                'ludwig.maximilian@outlook.de',
                'Ludwig Maximilian',
                (1985, 5, 12),
                '01732421123',
                'Maximilianstrasse 12',
                'München',
                '80539'
            ),
            (
                'xxALIxxstone@hotmail.com',
                'Albert Einstein',
                (1879, 3, 14),
                '01763425656',
                'Blumengasse 23',
                'Hamburg',
                '83452'
            ),
            (
                'mariecurry53@hotmail.com',
                'Marie Curie',
                (1867, 11, 7),
                '0174565656',
                'Jungfernstieg 2',
                'Hamburg',
                '34264'
            ),
            (
                'max.mustermann@gmail.com',
                'Maximilian Gustav Mustermann',
                (1997, 10, 23),
                '0176349756',
                'Schlossallee 100',
                'Grünwald',
                '82031'
            ),
            (
                'petergustav@gmail.com',
                'Peter Klaus Gustav von Guttenberg',
                (1995, 3, 11),
                '01763423732',
                'Leopoldstrasse 31',
                'Muenchen',
                '80238'
            ),
            (
                'gabi92@hotmail.com',
                'Gabriele Schwarz',
                (1998, 12, 10),
                '0175647332',
                'Kartoffelweg 12',
                'Muenchen',
                '80238'
            ),
            (
                'rudi343@gmail.com',
                'Rudolf Mayer',
                (1996, 5, 23),
                '01534423732',
                'Barerstrasse 3',
                'Muenchen',
                '80238'
            ),
            (
                'lea.g@gmx.com',
                'Lea Glas',
                (1985, 7, 11),
                '01763222732',
                'Argentinische Allee 34',
                'Hamburg',
                '34264'
            ),
            (
                'butterkeks@gmail.com',
                'Bettina Rupprecht',
                (1995, 10, 11),
                '01765673732',
                'Ordensmeisterstrasse 56',
                'Hamburg',
                '34264'
            ),
            (
                'willi.B@web.de',
                'Willi Birne',
                (1997, 6, 15),
                '01763425555',
                'Grunewaldstrasse 45',
                'Hamburg',
                '34264'
            ),
            (
                'pippi.langstrumpf@gmail.com',
                'Pippi Langstumpf',
                (1981, 7, 22),
                '01766767732',
                'Muehlenstraße 12',
                'Muenchen',
                '80238'
            )
        ]

        new_users = []
        for user in users:
            new_user = apimodels.UserProfile(email=user[0], name=user[1], phone_number=user[3], street=user[4],
                                          city=user[5], postal_code=user[6], rlc=rlc)
            new_user.birthday = AddMethods.generate_date(user[2])
            new_user.save()
            new_users.append(new_user)
        return new_users

    def create_groups(self, rlc, main_user, users):
        consultants = apimodels.Group(creator=main_user, from_rlc=rlc, name='Berater', visible=False,
                                   description='all consultants', note='only add consultants')
        consultants.save()
        consultants.group_members.add(users[0])
        consultants.group_members.add(users[1])
        consultants.group_members.add(users[2])
        consultants.group_members.add(users[3])
        consultants.group_members.add(users[4])
        consultants.group_members.add(users[5])
        consultants.group_members.add(users[6])
        consultants.group_members.add(users[7])
        consultants.group_members.add(users[8])
        consultants.save()
        self.add_permission_to_group(consultants, rlc, permissions.PERMISSION_CAN_CONSULT)
        self.add_permission_to_group(consultants, rlc, permissions.PERMISSION_VIEW_RECORDS_RLC)

        ag1 = apimodels.Group(creator=users[0], from_rlc=rlc, name='AG Datenschutz', visible=True, description='DSGVO',
                           note='bitte mithelfen')
        ag1.save()
        ag1.group_members.add(users[1])
        ag1.group_members.add(users[2])
        ag1.group_members.add(users[3])
        ag1.save()

        admins = apimodels.Group(creator=main_user, from_rlc=rlc, name='Administratoren', visible=False,
                              description='haben alle Berechtigungen', note='IT ressort')
        admins.save()
        admins.group_members.add(users[0])
        admins.group_members.add(main_user)
        admins.save()
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_VIEW_PERMISSIONS_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_MANAGE_PERMISSIONS_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_MANAGE_GROUPS_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_ACCEPT_NEW_USERS_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_PERMIT_RECORD_PERMISSION_REQUESTS_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_VIEW_RECORDS_FULL_DETAIL_RLC)
        self.add_permission_to_group(admins, rlc, permissions.PERMISSION_VIEW_RECORDS_RLC)

    def get_permission(self, permission):
        return apimodels.Permission.objects.get(name=permission)

    def add_permission_to_group(self, group, rlc, permission_name):
        has_permission = apimodels.HasPermission(group_has_permission=group, permission_for_rlc=rlc,
                                              permission=self.get_permission(permission_name))
        has_permission.save()

    def get_and_create_clients(self):
        origin_countries = list(models.OriginCountry.objects.all())
        clients = [
            (
                (2018, 7, 12),  # created_on
                (2018, 8, 28, 21, 3, 0, 0),  # last_edited
                'Bibi Aisha',  # name
                'auf Flucht von Ehemann getrennt worden',  # note
                '01793456542',  # phone number
                (1990, 5, 1),  # birthday
                random.choice(origin_countries)  # origin country id
            ),
            (
                (2017, 3, 17),
                (2017, 12, 24, 12, 2, 0, 0),
                'Mustafa Kubi',
                'möchte eine Ausbildung beginnen',
                '01456378963',
                (1998, 12, 3),
                random.choice(origin_countries)
            ),
            (
                (2018, 1, 1),
                (2018, 3, 3, 14, 5, 0, 0),
                'Ali Baba',
                'fragt wie er seine deutsche Freundin heiraten kann',
                '01345626534',
                (1985, 6, 27),
                random.choice(origin_countries)
            ),
            (
                (2018, 8, 1),
                (2018, 8, 2, 16, 3, 0, 0),
                'Kamila Iman',
                'möchte zu ihrer Schwester in eine andere Aufnahmeeinrichtung ziehen',
                '01562736778',
                (1956, 4, 3),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2017, 10, 2, 15, 3, 0, 0),
                'Junis Haddad',
                'Informationen zum Asylverfahren',
                '013345736778',
                (1998, 6, 2),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2018, 9, 2, 16, 3, 0, 0),
                'Nael Mousa',
                'Informationen zum Asylverfahren',
                '01444436778',
                (1997, 6, 4),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2018, 1, 12, 16, 3, 0, 0),
                'Amir Hamdan',
                'Informationen zum Asylverfahren',
                '01457636778',
                (1996, 6, 8),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2018, 1, 2, 16, 3, 0, 0),
                'Amar Yousef',
                'Informationen zum Asylverfahren',
                '01566546778',
                (1995, 5, 10),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2017, 12, 2, 16, 3, 0, 0),
                'Tarek Habib',
                'Informationen zum Asylverfahren',
                '013564736778',
                (1994, 5, 12),
                random.choice(origin_countries)
            ),
            (
                (2017, 9, 10),
                (2018, 10, 2, 16, 3, 0, 0),
                'Kaya Yousif',
                'Informationen zum Asylverfahren',
                '01564586778',
                (1993, 4, 14),
                random.choice(origin_countries)
            )
        ]
        clients_in_db = []
        for client in clients:
            clients_in_db.append(self.get_and_create_client(client))
        return clients_in_db

    def get_and_create_records(self, clients, consultants, rlc):
        tags = list(models.RecordTag.objects.all())
        records = [
            (
                random.choice(consultants),  # creator id
                (2018, 7, 12),  # created
                (2018, 8, 29, 13, 54, 0, 0),  # las edited
                clients[0],  # client
                (2018, 7, 10),  # first contact
                (2018, 8, 14, 17, 30, 0, 0),  # last contact
                'AZ-123/18',  # record token
                'informationen zum asylrecht',
                'cl',  # status, cl wa op
                [consultants[0], consultants[1]],  # working on
                [tags[0], tags[1]]  # tags
            ), (
                random.choice(consultants),
                (2018, 6, 23),
                (2018, 8, 22, 23, 3, 0, 0),
                clients[1],
                (2018, 6, 20),
                (2018, 7, 10, 17, 30, 0, 0),
                'AZ-124/18',
                'nicht abgeschlossen',
                'op',
                [consultants[0], consultants[2]],
                [tags[0], tags[12]]
            ), (
                random.choice(consultants),
                (2018, 8, 24),
                (2018, 8, 31, 1, 2, 0, 0),
                clients[2],
                (2018, 8, 22),
                (2018, 8, 22, 18, 30, 0, 0),
                'AZ-125/18',
                'auf Bescheid wartend',
                'wa',
                [consultants[0], consultants[3]],
                [tags[0], tags[11]]
            ), (
                random.choice(consultants),
                (2018, 3, 10),
                (2018, 4, 30, 19, 22, 0, 0),
                clients[3],
                (2018, 3, 9),
                (2018, 3, 24, 15, 54, 0, 0),
                'AZ-126/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'cl',
                [consultants[0], consultants[4]],
                [tags[0], tags[10]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2017, 10, 2, 15, 3, 0, 0),
                clients[4],
                (2017, 9, 10),
                (2017, 10, 2, 15, 3, 0, 0),
                'AZ-127/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'cl',
                [consultants[0], consultants[5]],
                [tags[1], tags[2]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2018, 9, 2, 16, 3, 0, 0),
                clients[5],
                (2017, 9, 10),
                (2018, 9, 2, 16, 3, 0, 0),
                'AZ-128/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'wa',
                [consultants[1], consultants[2]],
                [tags[1], tags[3]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2018, 1, 12, 16, 3, 0, 0),
                clients[6],
                (2017, 9, 10),
                (2018, 1, 12, 16, 3, 0, 0),
                'AZ-129/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'op',
                [consultants[1], consultants[3]],
                [tags[2], tags[4]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2018, 1, 2, 16, 3, 0, 0),
                clients[7],
                (2017, 9, 10),
                (2018, 1, 2, 16, 3, 0, 0),
                'AZ-130/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'cl',
                [consultants[2], consultants[5]],
                [tags[1], tags[5]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2018, 12, 2, 16, 3, 0, 0),
                clients[8],
                (2017, 9, 10),
                (2018, 12, 2, 16, 3, 0, 0),
                'AZ-131/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'wa',
                [consultants[3], consultants[4]],
                [tags[0], tags[7]]
            ), (
                random.choice(consultants),
                (2017, 9, 10),
                (2018, 10, 2, 16, 3, 0, 0),
                clients[9],
                (2017, 9, 10),
                (2018, 10, 2, 16, 3, 0, 0),
                'AZ-132/18',
                'Frau noch im Herkunftsland, gut recherchiert und ausfuehrlich dokumentiert',
                'op',
                [consultants[5], consultants[4]],
                [tags[3], tags[4]]
            )
        ]
        records_in_db = []
        for rec in records:
            records_in_db.append(self.get_and_create_record(rec, rlc))
        return records_in_db

    def get_and_create_client(self, client):
        cl = models.Client(name=client[2], note=client[3], phone_number=client[4])
        cl.created_on = AddMethods.generate_date(client[0])
        cl.last_edited = AddMethods.generate_datetime(client[1])
        cl.birthday = AddMethods.generate_date(client[5])
        cl.origin_country = client[6]
        cl.save()
        return cl

    def get_and_create_record(self, record_data, rlc):
        record = models.Record(from_rlc=rlc, creator=record_data[0], client=record_data[3], record_token=record_data[6],
                               official_note=record_data[7], state=record_data[8])
        record.created_on = AddMethods.generate_date(record_data[1])
        record.first_contact_date = AddMethods.generate_date(record_data[4])
        record.last_edited = AddMethods.generate_datetime(record_data[2])
        record.last_contact_date = AddMethods.generate_datetime(record_data[5])
        record.save()
        for user in record_data[9]:
            record.working_on_record.add(user)
        for tag in record_data[10]:
            record.tagged.add(tag)
        record.save()
        return record

        # random.choice[consultants],  # creator id
        # (2018, 7, 12),  # created
        # (2018, 8, 29, 13, 54, 0, 0),  # las edited
        # clients[0],  # client
        # (2018, 7, 10),  # first contact
        # (2018, 8, 14, 17, 30, 0, 0),  # last contact
        # 'AZ-123/18',  # record token
        # 'informationen zum asylrecht',
        # 'cl',  # status, cl wa op
        # [consultants[0], consultants[1]],  # working on
        # [tags[0], tags[1]]  # tags
