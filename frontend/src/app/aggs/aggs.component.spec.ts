import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggsComponent } from './aggs.component';

describe('AggsComponent', () => {
  let component: AggsComponent;
  let fixture: ComponentFixture<AggsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AggsComponent]
    });
    fixture = TestBed.createComponent(AggsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
