# https://github.com/elishaterada/heroku-google-application-credentials-buildpack/issues/2
echo ${GOOGLE_CREDENTIALS} > /app/google-credentials.json
