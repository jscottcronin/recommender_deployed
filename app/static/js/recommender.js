async function submit_async_rec_request(user_id) {
    // Execute POST request
    const response = await fetch('/rec_predict', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': user_id,
            'n_rec': 26,
            'execute_popularity': false
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        renderError();
        return
    }
    const results = await response.json();
    render_personalized_recs(results)
}

async function submit_async_popularity_request(user_id) {
    // Execute POST request
    const response = await fetch('/rec_predict', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': user_id,
            'n_rec': 26,
            'execute_popularity': true
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        renderError();
        return
    }
    const results = await response.json();
    render_popularity_recs(results)
}

async function submit_async_past_likes_request(user_id) {
    // Execute POST request
    const response = await fetch('/get_historical_likes', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': user_id,
            'n': 26
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        renderError();
        return
    }
    const results = await response.json();
    render_past_likes(results)
}



function renderError() {
    $('#errorAlert').text('Oooopsies. There was an issue with this user.').show();
    $('#successAlert').hide();
}
//
function render_past_likes(results) {
    $('#errorAlert').hide();
    $('#past_likes').show();
    $('#past_likes_posters')
        // equivalent to python lambda function
        .html(results['posters'].map(img => renderResult(img)).join(''))
        .show()
}

function render_personalized_recs(results) {
    $('#errorAlert').hide();
    $('#recs').show();
    $('#personalized_recs')
        // equivalent to python lambda function
        .html(results['posters'].map(img => renderResult(img)).join(''))
        .show()
}

function render_popularity_recs(results) {
    $('#errorAlert').hide();
    $('#popular').show();
    $('#popular_posters')
        // equivalent to python lambda function
        .html(results['posters'].map(img => renderResult(img)).join(''))
        .show()
}
//
// // Generate Formatted HTML to show subcategories
function renderResult(poster_url) {

    return `
        <img src="${poster_url}" class="img-thumbnail">
    `;
}


$(() => {
    $(document).on('click', '.rounded-circle', (ev) => {
        ev.preventDefault()
        const userId = Number(ev.target.id)
        submit_async_rec_request(userId)
        submit_async_popularity_request(userId)
        submit_async_past_likes_request(userId)
    });
})
