// returns client instance to perform api requests
export function getClient(coreapi) {
    // instead of getCookies
    let auth = new coreapi.auth.SessionAuthentication({
      csrfCookieName: 'csrftoken',
      csrfHeaderName: 'X-CSRFToken',
    });
    // If you have logged in previously it'll reflect the changes 
    const client = new coreapi.Client({auth: auth});
  return client;
}