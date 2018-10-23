/*
 * rlcapp - record and organization management software for refugee law clinics
 * Copyright (C) 2018  Dominik Walser
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>
 ******************************************************************************/

import { Component, OnInit } from "@angular/core";
import {FullRecord, RestrictedRecord} from '../../../models/record.model';
import {RecordsSandboxService} from '../../../services/records-sandbox.service';
import {FullClient} from '../../../models/client.model';
import {OriginCountry} from '../../../models/country.model';

@Component({
    selector: "app-restricted-record-detail",
    templateUrl: "./restricted-record-detail.component.html",
    styleUrls: ["./restricted-record-detail.component.scss"]
})
export class RestrictedRecordDetailComponent implements OnInit {
    record: RestrictedRecord;

    constructor(private recordSB: RecordsSandboxService) {}

    ngOnInit() {
        this.recordSB
            .getSpecialRecord()
            .subscribe(
                (special_record: {
                    record: RestrictedRecord;
                }) => {
                    this.record = special_record.record;
                }
            );
    }
}
