import { Component, OnInit } from '@angular/core';
import {Role} from '../../models/Role';
import {DataService} from '../../services/data.service';

@Component({
  selector: 'app-role-dashboard',
  templateUrl: './role-dashboard.component.html',
  styleUrls: ['./role-dashboard.component.css']
})
export class RoleDashboardComponent implements OnInit {

  // Bar chat config
  barData: any[];
  barView: any[] = [700, 400];

  // options
  barShowXAxis = true;
  barShowYAxis = true;
  barGradient = false;
  barShowLegend = true;
  barShowXAxisLabel = true;
  barXAxisLabel = 'Virtue';
  barShowYAxisLabel = true;
  barYAxisLabel = 'Migrations Today';

  barColorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  // Table Config
  cols = [
    { field: 'cid', header: 'Id'},
    { field: 'dn', header: 'Domain Name' },
    { field: 'ou', header: 'Organizational Unit' },
    { field: 'name', header: 'Role Name' },
    { field: 'cstate', header: 'State' },
    { field: 'cversion', header: 'Version' }
  ];

  tableData: Role[];
  barData: any[];

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getVirtuesPerRole().subscribe(
      response => this.barData = this.buildBarData(response)
    );

    this.dataService.getRoles().subscribe(
      roles => (
        this.tableData = this.parseArrays(roles)));

    // this.tableData = [
    //   {
    //     dn: 'cusername=fpatwa,cn=users,ou=virtue,dc=canvas,dc=virtue,dc=com',
    //     ou: 'virtue',
    //     cid: 'Virtue_SecurityTestRole_1539878119',
    //     name: 'TestRole',
    //     cstate: 'CREATED',
    //     version: '1.0',
    //     cappIds: [],
    //     cresIds: [],
    //     ctransIds: []
    //   }
    // ];
  }

  private buildBarData(response: any): any {
    const data = [];
    for (const key in response) {
      if (response.hasOwnProperty(key)) {
        const obj = {};
        obj['name'] = key;
        obj['value'] = response[key];
        data.push(obj);
      }
    }
    return data;
  }

  private parseArrays(roles: Role[]): Role[] {
    for (let role of roles) {
      try {
        role.cappIds = JSON.parse(role.cappIds.replace(/\'/g, '\"'));
      } catch (e) {
        console.log(e);
        role.cappIds = ['ERROR_PROCESSING_JSON'];
      }
      try {
        role.cstartResIds = JSON.parse(role.cstartResIds.replace(/\'/g, '\"'));
      } catch (e) {
        console.log(e);
        role.cstartResIds = ['ERROR_PROCESSING_JSON'];
      }
      try {
        role.cstartTransIds = JSON.parse(role.cstartTransIds.replace(/\'/g, '\"'));
      } catch (e) {
        console.log(e);
        role.cstartTransIds = ['ERROR_PROCESSING_JSON'];
      }
    }
    return roles;
  }
)
}