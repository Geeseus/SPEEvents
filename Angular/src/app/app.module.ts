import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { EventDisplayComponent } from './event-display/event-display.component';
import { EventListComponent } from './eventlist/eventlist.component';
import { UserListComponent } from './userlist/userlist.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from "@angular/material/button";
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from "@angular/material/toolbar";
import { SPEDataModule } from 'spedata';

@NgModule({
  declarations: [
    AppComponent,
    EventDisplayComponent,
    EventListComponent,
    UserListComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatExpansionModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    SPEDataModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
