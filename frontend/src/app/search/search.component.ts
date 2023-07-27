import { Component } from '@angular/core';
import { SearchService } from '../search.service';
import { trigger, transition, style, animate, AnimationTriggerMetadata } from '@angular/animations';
import { setFadeInOut } from '../app.animation';


interface SearchResult {
  title: string
  director: string
  cast: string[]
  country: string
  date_added: string
  release_year: number
  rating: string
  duration: number
  genres: string[]
  description: string
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
  animations: [setFadeInOut]
})
export class SearchComponent {
  private nullSearch = {title: "", director: "", cast: [], country: "",
                        date_added: "", release_year: -1, rating: "",
                        duration: -1, genres: [], description: ""};
  filmType: string = "movie";
  searchText: string = "";
  searchResult: SearchResult = this.nullSearch;
  isSearching: boolean = false;
  validResults: boolean = true;

  constructor(private searchService: SearchService) {}

  isCastArray(): boolean {
    return Array.isArray(this.searchResult.cast);
  }
  isGenreArray(): boolean {
    return Array.isArray(this.searchResult.genres);
  }

  onFilmTypeChange() {
    this.onSearch();
  }

  whileTyping() {
    this.searchResult = this.nullSearch;
  }

  enterKey(event: KeyboardEvent) {
    if (event.key == 'Enter' && this.searchText) {
      this.onSearch();
    }
  }

  onSearch() {
    this.isSearching = true;
    this.searchService.getSearchData(this.filmType, this.searchText).subscribe(
      (result: SearchResult) => {
        this.searchResult = result;
        // Update date to be human readable
        if (this.searchResult.date_added) {
          var date = this.searchResult.date_added.slice(0, 2) + '/' + this.searchResult.date_added.slice(2);
          date = date.slice(0, 5) + '/' + date.slice(5);
          this.searchResult.date_added = date;
        }
        // Determine if results came back empty
        if (!this.searchResult.title) {
          this.validResults = false;
        } else {
          this.validResults = true;
        }
        this.isSearching = false;
      },
      (error) => {
        this.searchResult = {'title': 'Some title',
        'director': 'Herman Yau',
        'cast': ['Francis Chun-Yu Ng',
         'Louis Koo',
         'Anita Yuen',
         'Tat-Ming Cheung',
         'Jocelyn Choi',
         'Ng Siu-hin',
         'Lam Suet',
         'Anthony Wong Chau-Sang',
         'Lo Hoi-pang'],
        'country': 'Hong Kong',
        'date_added': '04302019',
        'release_year': 2019,
        'rating': 'TV-MA',
        'duration': 92,
        'genres': ['Comedies', 'International Movies'],
        'description': 'When a neighbor blocks their view of the city with a commercial billboard, a Hong Kong family resorts to drastic, imaginative measures to take it down.'};
        
        // Update date to be human readable
        if (this.searchResult.date_added) {
          var date = this.searchResult.date_added.slice(0, 2) + '/' + this.searchResult.date_added.slice(2);
          date = date.slice(0, 5) + '/' + date.slice(5);
          this.searchResult.date_added = date;
        }


        console.error('Error fetching data:', error);
        this.isSearching = false;
      }
    )
  }

}

