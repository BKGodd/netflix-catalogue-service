import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { Component } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';

@Component({
  selector: 'app-search',
  template: 'App Search Component',
})
class AppSearchComponent {}

@Component({
  selector: 'app-aggs',
  template: 'App Aggs Component',
})
class AppAggsComponent {}

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent, AppSearchComponent, AppAggsComponent],
      imports: [HttpClientTestingModule],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the app component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize showSearchContent to true and showAggsContent to false', () => {
    expect(component.showSearchContent).toBe(true);
    expect(component.showAggsContent).toBe(false);
  });

  it('should set showSearchContent to true and showAggsContent to false when calling loadSearchContent()', () => {
    component.loadSearchContent();

    expect(component.showSearchContent).toBe(true);
    expect(component.showAggsContent).toBe(false);
  });

  it('should set showAggsContent to true and showSearchContent to false when calling loadAggsContent()', () => {
    component.loadAggsContent();

    expect(component.showAggsContent).toBe(true);
    expect(component.showSearchContent).toBe(false);
  });

  it('should display the "app-search" component when showSearchContent is true', () => {
    component.loadSearchContent();
    fixture.detectChanges();
    const appSearchElement = fixture.nativeElement.querySelector('app-search');
    const appAggsElement = fixture.nativeElement.querySelector('app-aggs');
    expect(appSearchElement).toBeTruthy();
    expect(appAggsElement).toBeFalsy();
  });
  
  it('should display the "app-aggs" component when showAggsContent is true', () => {
    component.loadAggsContent();
    fixture.detectChanges();
    const appAggsElement = fixture.nativeElement.querySelector('app-aggs');
    const appSearchElement = fixture.nativeElement.querySelector('app-search');
    expect(appAggsElement).toBeTruthy();
    expect(appSearchElement).toBeFalsy();
  });
});
