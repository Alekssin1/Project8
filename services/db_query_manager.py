from django.shortcuts import get_object_or_404
from games.models import Game, Genre, Review
from django.db.models import Min

class DBQueryManager:
    @staticmethod
    def get_all_games():
        return Game.objects.all()

    @staticmethod
    def get_games_by_genre(genre_filter):
        return Game.objects.filter(genres__name=genre_filter)

    @staticmethod
    def get_all_genres():
        return Genre.objects.all()

    @staticmethod
    def get_game_by_id(game_id):
        return get_object_or_404(Game, pk=game_id)

    @staticmethod
    def search_games_by_keyword(keyword):
        if keyword:
            return Game.objects.filter(title__icontains=keyword)
        return None

    @staticmethod
    def get_random_discount_game():
        return Game.objects.filter(discount_price__isnull=False).order_by('?').first()

    @staticmethod
    def get_most_popular_games():
        return Game.objects.order_by('-downloads')[:4]

    @staticmethod
    def get_latest_games():
        return Game.objects.order_by('-id')[:4]

    @staticmethod
    def get_genres_with_random_games():
        return Genre.objects.annotate(
            random_game_image=Min('games__image')
        ).values('name', 'random_game_image')
    
    @staticmethod
    def get_game_with_reviews_and_related(game_id):
        game = get_object_or_404(Game, pk=game_id)

        reviews = Review.objects.filter(game=game).select_related('user')
        reviews_with_user_info = [{'user': review.user, 'name': review.user.name, 'surname': review.user.surname, 'comment': review.comment} for review in reviews]

        related_by_genre = Game.objects.filter(genres__in=game.genres.all()).exclude(pk=game_id).distinct()

        related_by_tags = Game.objects.filter(tags__in=game.tags.all()).exclude(pk=game_id).distinct()

        related_by_developer = Game.objects.filter(developers__in=game.developers.all()).exclude(pk=game_id).distinct()

        return game, reviews_with_user_info, related_by_genre, related_by_tags, related_by_developer