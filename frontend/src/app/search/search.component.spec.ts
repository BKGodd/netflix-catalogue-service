import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { SearchComponent, SearchResult } from './search.component';
import { SearchService } from '../search.service';

describe('SearchComponent', () => {
  let component: SearchComponent;
  let fixture: ComponentFixture<SearchComponent>;
  let mockSearchService: jasmine.SpyObj<SearchService>;

  beforeEach(() => {
    const searchServiceSpy = jasmine.createSpyObj('SearchService', ['getSearchData']);
    TestBed.configureTestingModule({
      declarations: [SearchComponent],
      providers: [
        { provide: SearchService, useValue: searchServiceSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(SearchComponent);
    component = fixture.componentInstance;
    mockSearchService = TestBed.inject(SearchService) as jasmine.SpyObj<SearchService>;
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should test if cast response is a proper array', () => {
    component.searchResult = [component.nullSearch];
    component.searchResult[0].cast = null;
    expect(component.isCastArray(0)).toEqual(false);

    component.searchResult[0].cast = [];
    expect(component.isCastArray(0)).toEqual(true);
  });

  it('should test if genres response is a proper array', () => {
    component.searchResult = [component.nullSearch];
    component.searchResult[0].genres = null;
    expect(component.isGenreArray(0)).toEqual(false);

    component.searchResult[0].genres = [];
    expect(component.isGenreArray(0)).toEqual(true);
  });

  it('should test an empty search result', () => {
    const filmType = 'movie';
    const searchText = '';
    const mockSearchResult = component.nullSearch;

    mockSearchService.getSearchData.and.returnValue(of(mockSearchResult));

    // Perform search
    component.filmType = filmType;
    component.searchText = searchText;
    component.onSearch();
  
    // Check that we did not obtain valid results to display (empty)
    expect(component.searchResult).toEqual(mockSearchResult);
    expect(component.isSearching).toBeFalse();
    expect(component.validResults).toBeFalse();
    expect(component.errorRequest).toBeFalse();
  
    // Check that the getSearchData method was called with the correct parameters
    expect(mockSearchService.getSearchData).toHaveBeenCalledWith(filmType, searchText);
  });

  it('should test a valid search result', () => {
    const filmType = 'movie';
    const searchText = 'parks';
    const mockSearchResult: SearchResult[] = [{title: 'Parks and Recreation',
                                            director: '',
                                            cast: ['Amy Poehler',
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
                                            country: 'United States',
                                            date_added: '01132016',
                                            release_year: 2015,
                                            rating: 'TV-14',
                                            duration: 7,
                                            genres: ['TV Comedies'],
                                            description: 'In this Emmy-nominated comedy, an employee with a rural Parks and Recreation department is full of energy and ideas but bogged down by bureaucracy.'}];

    mockSearchService.getSearchData.and.returnValue(of(mockSearchResult));

    // Perform search
    component.filmType = filmType;
    component.searchText = searchText;
    component.onSearch();
  
    // Check that we did obtain valid results to display (not empty)
    console.log(component.searchResult)
    expect(component.searchResult).toEqual(mockSearchResult);
    expect(component.isSearching).toBeFalse();
    expect(component.validResults).toBeTrue();
    expect(component.errorRequest).toBeFalse();
  
    // Check that the getSearchData method was called with the correct parameters
    expect(mockSearchService.getSearchData).toHaveBeenCalledWith(filmType, searchText);
  });
  
  it('should test a correctly formatted date from the response', () => {
    const filmType = 'movie';
    const searchText = 'parks';
    const rawDate = '01132016';
    const correctDate = '01/13/2016';
    const mockSearchResult: SearchResult = {title: 'Some title',
                                            director: '',
                                            cast: ['Some actor'],
                                            country: 'United States',
                                            date_added: rawDate,
                                            release_year: 2015,
                                            rating: 'TV-14',
                                            duration: 7,
                                            genres: ['TV Comedies'],
                                            description: 'Some description.'};

    mockSearchService.getSearchData.and.returnValue(of(mockSearchResult));

    // Perform search
    component.filmType = filmType;
    component.searchText = searchText;
    component.onSearch();
  
    // Check that the date has been reformatted correctly
    expect(component.searchResult.date_added).toEqual(correctDate);
  
    // Check that the getSearchData method was called with the correct parameters
    expect(mockSearchService.getSearchData).toHaveBeenCalledWith(filmType, searchText);
  });

  it('should handle error on onSearch', () => {
    // Set the return value for the getSearchData spy to throw an error
    const errorMessage = 'Mock Error';
    mockSearchService.getSearchData.and.returnValue(throwError(errorMessage));

    // Initial values before calling onSearch
    component.searchText = 'search_query';
    component.searchResult = { title: 'Title',
                                director: 'Director',
                                cast: [],
                                country: 'Country',
                                date_added: '2023-07-01',
                                release_year: 2023,
                                rating: 'PG-13',
                                duration: 120,
                                genres: [],
                                description: 'Description' };
    component.isSearching = false;
    component.validResults = true;
    component.errorRequest = false;

    spyOn(console, 'error');

    component.onSearch();

    expect(component.searchResult).toEqual(component.nullSearch);
    expect(component.errorRequest).toBeTrue();
    expect(component.isSearching).toBeFalse();

    // Check if the console.error is called with the correct error message
    expect(console.error).toHaveBeenCalledWith('Error fetching data:', errorMessage);
  });

});
