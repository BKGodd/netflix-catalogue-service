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
  searchResult: SearchResult = this.nullSearch;
  isSearching: boolean = false;
  validResults: boolean = true;
  errorRequest: boolean = false;

  constructor(private searchService: SearchService) {}

  isCastArray(): boolean {
    return Array.isArray(this.searchResult.cast) && this.searchResult.cast.length > 0;
  }
  isGenreArray(): boolean {
    return Array.isArray(this.searchResult.genres) && this.searchResult.genres.length > 0;
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
        this.errorRequest = false;
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
        this.searchResult = this.nullSearch;
        this.errorRequest = true;
        console.error('Error fetching data:', error);
        this.isSearching = false;
      }
    )
  }
}
