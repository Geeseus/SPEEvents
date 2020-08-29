import { NgModule } from '@angular/core';
import { EventArchiveService } from './event-archive.service';
import { EventDataService } from './event-data.service';
import { UserDataService } from './user-data.service';

import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [],
  imports: [ HttpClientModule ],
  exports: [],
  providers: [
    { provide: 'EVENT_ARCHIVE_URL', useValue: 'https://events.shitpostemblem.xyz/data/archive.json' },
    EventArchiveService,
    { provide: 'EVENT_DATA_URL', useValue: 'https://events.shitpostemblem.xyz/data/events.json' },
    EventDataService,
    { provide: 'USER_DATA_URL', useValue: 'https://events.shitpostemblem.xyz/data/users.json' },
    UserDataService]
})
export class SPEDataModule { }
