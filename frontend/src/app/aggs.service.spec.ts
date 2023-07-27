import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AggsService } from './aggs.service';

describe('AggsService', () => {
  let service: AggsService;
  let httpMock: HttpTestingController;
  const host = 'http://127.0.0.1:5400';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AggsService]
    });
    service = TestBed.inject(AggsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get data from the server for total', () => {
    const expectedRes = {'director_agg': {'Rajiv Chilaka': 19,
                          'Raul Campos Jan Suter': 18,
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
    service.getData().total.subscribe(
      (data) => {
        expect(data).toEqual(service.cleanData(expectedRes));
      }
    );

    const req = httpMock.expectOne('/api/aggs/');
    expect(req.request.method).toBe('GET');
    req.flush(expectedRes);
  });

  it('should get data from the server for movie', () => {
    const expectedData = {'histo_dur_agg': {'0': 25,
                          '20': 144,
                          '40': 288,
                          '60': 592,
                          '80': 2156,
                          '100': 1724,
                          '120': 770,
                          '140': 271,
                          '160': 108,
                          '180': 29,
                          '200': 11},
                        'avg_dur_agg': 99,
                        'total_agg': 6131};
    service.getData().movie.subscribe(
      (data) => {
        expect(data).toEqual(service.cleanData(expectedData));
      }
    );

    const req = httpMock.expectOne('/api/aggs/movie/');
    expect(req.request.method).toBe('GET');
    req.flush(expectedData);
  });

  it('should get data from the server for show', () => {
    const expectedData = {'total_agg': 2676};
    service.getData().show.subscribe(
      (data) => {
        expect(data).toEqual(service.cleanData(expectedData));
      },
    );

    const req = httpMock.expectOne('/api/aggs/show/');
    expect(req.request.method).toBe('GET');
    req.flush(expectedData);
  });
});
