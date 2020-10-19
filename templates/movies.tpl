<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Studio Ghibli Movies</title>
    </head>
    <body>
        <h2>Studio Ghibli movies</h2>
        <ul>
        % if movies:
          % for movie in movies.values():
            <li>{{movie.get('title')}}</li>
            <ul>
            % for actor in movie.get('people'):
                <li>{{actor.get('name')}}</li>
            % end
            </ul>
          % end
        % end
        </ul>
        <p>Updated at : {{updated_at.strftime('%c') if updated_at is not None else ''}}</p>
    </body>
</html>
