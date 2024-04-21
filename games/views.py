from django.shortcuts import render
from django.views import View
from mailing.forms import SubscribeForm
from services.db_query_manager import DBQueryManager

class AppRenderView(View):
    def get(self, request):
        return render(request, "contact.html")

class ShopView(View):
    def get(self, request):
        genre_filter = request.GET.get('genre')
        if genre_filter:
            games = DBQueryManager.get_games_by_genre(genre_filter)
        else:
            games = DBQueryManager.get_all_games()

        genres = DBQueryManager.get_all_genres()

        context = {
            'games': games,
            'genres': genres,
            'selected_genre': genre_filter
        }

        return render(request, 'shop.html', context)

class ProductView(View):
    def get(self, request, game_id):
        game, reviews, related_by_genre, related_by_tags, related_by_developer = DBQueryManager.get_game_with_reviews_and_related(game_id)
        review_count = len(reviews)
        return render(request, "product-details.html", {
            'game': game,
            'reviews': reviews,
            'review_count': review_count,
            'related_by_genre': related_by_genre,
            'related_by_tags': related_by_tags,
            'related_by_developer': related_by_developer
        })

class SearchView(View):
    def post(self, request):
        search_keyword = request.POST.get('searchKeyword')
        results = DBQueryManager.search_games_by_keyword(search_keyword)
        return render(request, 'search.html', {'results': results})

    def get(self, request):
        return render(request, 'search.html', {'results': None})

class HomeView(View):
    def get(self, request):
        random_discount_game = DBQueryManager.get_random_discount_game()
        discount_percentage = 100 * (random_discount_game.price - random_discount_game.discount_price) / random_discount_game.price
        genres_with_random_games = DBQueryManager.get_genres_with_random_games()
        most_popular_games = DBQueryManager.get_most_popular_games()
        latest_games = DBQueryManager.get_latest_games()
        form = SubscribeForm()

        context = {
            'random_game': random_discount_game,
            'discount_percentage': discount_percentage,
            'genres_with_random_games': genres_with_random_games,
            'most_popular_games': most_popular_games,
            'latest_games': latest_games,
            'form': form,
        }
        return render(request, "index.html", context)