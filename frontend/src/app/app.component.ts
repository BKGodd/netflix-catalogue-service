import { Component, OnInit } from '@angular/core';
import { AggsService } from './aggs.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  showSearchContent: boolean = true;
  showAggsContent: boolean = false;

  loadSearchContent() {
    this.showSearchContent = true;
    this.showAggsContent = false;
  }

  loadAggsContent() {
    this.showAggsContent = true;
    this.showSearchContent = false;
  }
}
