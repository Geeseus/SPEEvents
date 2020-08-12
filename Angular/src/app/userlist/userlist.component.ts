import { Component, OnInit, ViewChild } from '@angular/core';
import { UserData, UserDataService } from "dist/spedata";
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-userlist',
  templateUrl: './userlist.component.html',
  styleUrls: ['./userlist.component.css']
})
export class UserListComponent implements OnInit {

  public columns: string[] = ['name', 'points'];
  public userDataSource: MatTableDataSource<UserData>;
  @ViewChild(MatSort, {static: true}) public sort: MatSort;

  constructor(private dataService: UserDataService) { }

  ngOnInit(): void {
    this.dataService.getUsers().subscribe((userData: UserData[]) => {
      this.userDataSource = new MatTableDataSource(userData);
      this.userDataSource.sort = this.sort;
    });
  }

}
