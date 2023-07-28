import { Component } from '@angular/core';
import { SearchService } from '../search.service';
import { setFadeInOut } from '../app.animation';


export interface SearchResult {
  title: string | null
  director: string | null
  cast: string[] | null
  country: string | null
  date_added: string | null
  release_year: number | null
  rating: string | null
  duration: number | null
  genres: string[] | null
  description: string | null
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
  animations: [setFadeInOut]
})
export class SearchComponent {
  nullSearch = {title: "", director: "", cast: [], country: "",
                        date_added: "", release_year: -1, rating: "",
                        duration: -1, genres: [], description: ""};
  filmType: string = "movie";
  searchText: string = "";
  searchResult: SearchResult[] = [];
  isSearching: boolean = false;
  validResults: boolean = true;
  errorRequest: boolean = false;
  anim_delays: number[] = Array.from({ length: 8 }, (_, index) => (index + 1) * 100);

  constructor(private searchService: SearchService) {}

  
  isCastArray(index: number): boolean {
    return Array.isArray(this.searchResult[index].cast) &&
      this.searchResult[index].cast!.length > 0;
  }
  isGenreArray(index: number): boolean {
    return Array.isArray(this.searchResult[index].genres) &&
      this.searchResult[index].genres!.length > 0;
  }

  onFilmTypeChange() {
    this.searchResult = [];
  }

  whileTyping() {
    this.searchResult = [];
  }

  enterKey(event: KeyboardEvent) {
    if (event.key == 'Enter' && this.searchText) {
      this.onSearch();
    }
  }

  onSearch() {
    this.isSearching = true;
    this.searchService.getSearchData(this.filmType, this.searchText).subscribe(
      (result: SearchResult[]) => {
        this.searchResult = result;
        if (this.searchResult.length == 0) {
          this.validResults = false;
        } else {
          this.validResults = true;
          this.errorRequest = false;
          // Turn date_added into a human readable date
          for (let i = 0; i < this.searchResult.length; i++) {
            if (typeof this.searchResult[i].date_added == "string" ) {
              var date = this.searchResult[i].date_added!.slice(0, 2) + '/' + this.searchResult[i].date_added!.slice(2);
              date = date.slice(0, 5) + '/' + date.slice(5);
              this.searchResult[i].date_added = date;
            }
          }
        }
      },
      (error) => {
        this.searchResult = [{'title': 'Aziz Ansari Live at Madison Square Garden',
        'director': 'Aziz Ansari',
        'cast': ['Aziz Ansari'],
        'country': 'United States',
        'date_added': '03062015',
        'release_year': 2015,
        'rating': 'TV-MA',
        'duration': 58,
        'genres': [],
        'description': 'Stand-up comedian and TV star Aziz Ansari ("Parks and Recreation") delivers his sharp-witted take on immigrants, relationships and the food industry.'},
       {'title': 'Aziz Ansari: Buried Alive',
        'director': 'Will Lovelace Dylan Southern',
        'cast': [],
        'country': 'United States',
        'date_added': '11012013',
        'release_year': 2013,
        'rating': 'TV-MA',
        'duration': 80,
        'genres': ['StandUp Comedy'],
        'description': '"Parks and Recreation" star Aziz Ansari takes the stage to share his unfiltered views on adulthood, babies, marriage, love and more in the modern era.'}];
        this.errorRequest = true;
        this.isSearching = false;
        this.validResults = true;
        console.error('Error fetching data:', error);
      }
    )
  }
}
