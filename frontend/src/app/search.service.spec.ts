import { TestBed } from '@angular/core/testing';
import { SearchService } from './search.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('SearchService', () => {
  let service: SearchService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SearchService]
    });
    service = TestBed.inject(SearchService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should test an HTTP GET request and get a valid response for a show', () => {
    const filmType = 'show';
    const searchText = 'parks and recreation';
    const expectedRes = {'title': 'Parks and Recreation',
                          'director': null,
                          'cast': ['Amy Poehler',
                            'Rashida Jones',
                            'Aziz Ansari',
                            'Nick Offerman',
                            'Aubrey Plaza',
                            'Chris Pratt',
                            'Jim OHeir',
                            'Retta',
                            'Adam Scott',
                            'Rob Lowe',
                            'Paul Schneider'],
                          'country': 'United States',
                          'date_added': '01132016',
                          'release_year': 2015,
                          'rating': 'TV-14',
                          'duration': 7,
                          'genres': ['TV Comedies'],
                          'description': 'In this Emmy-nominated comedy, an employee with a rural Parks and Recreation department is full of energy and ideas but bogged down by bureaucracy.'}

    service.getSearchData(filmType, searchText).subscribe(
      (response) => {
        expect(response).toEqual(expectedRes);
      }
    );

    const req = httpMock.expectOne(`/api/film/${filmType}/?query=${encodeURIComponent(searchText)}`);
    expect(req.request.method).toBe('GET');
    req.flush(expectedRes);
  });

  it('should test an HTTP GET request and get a valid response for a movie', () => {
    const filmType = 'movie';
    const searchText = 'parks and recreation';
    const expectedRes = {'title': 'Aziz Ansari Live at Madison Square Garden',
                          'director': 'Aziz Ansari',
                          'cast': ['Aziz Ansari'],
                          'country': 'United States',
                          'date_added': '03062015',
                          'release_year': 2015,
                          'rating': 'TV-MA',
                          'duration': 58,
                          'genres': ['StandUp Comedy'],
                          'description': 'Stand-up comedian and TV star Aziz Ansari ("Parks and Recreation") delivers his sharp-witted take on immigrants, relationships and the food industry.'}

    service.getSearchData(filmType, searchText).subscribe(
      (response) => {
        expect(response).toEqual(expectedRes);
      }
    );

    const req = httpMock.expectOne(`/api/film/${filmType}/?query=${encodeURIComponent(searchText)}`);
    expect(req.request.method).toBe('GET');
    req.flush(expectedRes);
  });

  it('should test an HTTP GET request with empty query parameter', () => {
    const filmType = 'show';
    const searchText = '';
    const expectedRes = {'title': '',
                          'director': '',
                          'cast': [],
                          'country': '',
                          'date_added': '',
                          'release_year': -1,
                          'rating': '',
                          'duration': -1,
                          'genres': [],
                          'description': ''}

    service.getSearchData(filmType, searchText).subscribe(
      next => {
        expect(next).toEqual(expectedRes);
      }
    );

    const req = httpMock.expectOne(`/api/film/${filmType}/?query=${searchText}`);
    expect(req.request.method).toBe('GET');
    req.flush(expectedRes);
  });
});
