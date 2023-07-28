import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  showSearchContent = true;
  showAggsContent = false;

  loadSearchContent() {
    this.showSearchContent = true;
    this.showAggsContent = false;
  }

  loadAggsContent() {
    this.showAggsContent = true;
    this.showSearchContent = false;
  }
}
