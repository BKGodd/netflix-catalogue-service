import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { AggsComponent } from './aggs.component';
import { AggsService } from '../aggs.service';

describe('AggsComponent', () => {
  let component: AggsComponent;
  let fixture: ComponentFixture<AggsComponent>;
  let mockAggsService: jasmine.SpyObj<AggsService>;

  beforeEach(() => {
    // Create a spy object for AggsService
    const spy = jasmine.createSpyObj('AggsService', ['getData']);

    TestBed.configureTestingModule({
      declarations: [AggsComponent],
      providers: [{ provide: AggsService, useValue: spy }],
    }).compileComponents();

    fixture = TestBed.createComponent(AggsComponent);
    component = fixture.componentInstance;
    mockAggsService = TestBed.inject(AggsService) as jasmine.SpyObj<AggsService>;
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should set aggResponse, aggMovieResponse, and aggShowResponse on ngOnInit', () => {
    // Define mock data for each observable
    const mockTotal = {'director_agg': {'Rajiv Chilaka': 19,
                        'Raúl Campos, Jan Suter': 18,
                        'Marcus Raboy': 16,
                        'Suhas Kadav': 16,
                        'Jay Karas': 14},
                      'actor_agg': {'Anupam Kher': 43,
                        'Shah Rukh Khan': 35,
                        'Julie Tejwani': 33,
                        'Naseeruddin Shah': 32,
                        'Takahiro Sakurai': 32},
                      'rating_agg': {'TV-MA': 3207,
                        'TV-14': 2160,
                        'TV-PG': 863,
                        'R': 799,
                        'PG-13': 490},
                      'country_agg': {'United States': 2818,
                        'India': 972,
                        'United Kingdom': 419,
                        'Japan': 245,
                        'South Korea': 199},
                      'genre_agg': {'International Movies': 2752,
                        'Dramas': 2427,
                        'Comedies': 1674,
                        'International TV Shows': 1351,
                        'Documentaries': 869},
                      'total_agg': 8807};
    const mockMovie = {'histo_dur_agg': {'0': 25,
                        '20': 144,
                        '40': 288,
                        '60': 592,
                        '80': 2156,
                        '100': 1724,
                        '120': 770,
                        '140': 271,
                        '160': 108,
                        '180': 29,
                        '200': 11,
                        '220': 6,
                        '240': 1,
                        '260': 1,
                        '280': 0,
                        '300': 1},
                      'avg_dur_agg': 99,
                      'total_agg': 6131};
    const mockShow = {'total_agg': 2676};

    mockAggsService.getData.and.returnValue({
      total: of(mockTotal),
      movie: of(mockMovie),
      show: of(mockShow),
    });

    component.ngOnInit();

    // Ensure that the aggResponse, aggMovieResponse, and aggShowResponse are set correctly
    expect(component.aggResponse).toEqual(mockTotal);
    expect(component.aggMovieResponse).toEqual(mockMovie);
    expect(component.aggShowResponse).toEqual(mockShow);
  });

  it('should handle error on ngOnInit', () => {
    // Set the return values for the getData spy to throw an error
    mockAggsService.getData.and.returnValue({
      total: of({}),
      movie: of({}),
      show: throwError('Mock Error'),
    });

    // Use spyOn to spy on the console.log method to check for errors
    spyOn(console, 'log');

    // Call ngOnInit
    component.ngOnInit();

    // Ensure that the error is logged to the console
    expect(console.log).toHaveBeenCalledWith('Mock Error');
  });
});
