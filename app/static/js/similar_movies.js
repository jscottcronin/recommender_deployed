async function submit_async_sims_request(movie_id) {
    // Execute POST request
    const response = await fetch('/get_similar_movies', {
        method: 'POST',
        body: JSON.stringify({
            'movie_id': movie_id,
            'n': 40
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
    render_similar_movies(results)
    console.log("running result on ${movie_id}")
}


function renderError() {
    $('#errorAlert').text('Oooopsies. There was an issue with this movie.').show();
    $('#successAlert').hide();
}
//
function render_similar_movies(results) {
    $('#errorAlert').hide();
    $('#instructions').hide();
    $('#similarity_block').show();
    $('#similar_items')
        // equivalent to python lambda function
        .html(results['results'].map(result => renderResult(result)).join(''))
        .show()
}

//
// // Generate Formatted HTML to show subcategories
function renderResult(result) {
    return `
        <img src="${result[1]}" id="${result[0]}" class="img-thumbnail">
    `;
}


$(() => {
    $(document).on('click', '.img-thumbnail', (ev) => {
        ev.preventDefault()
        const movie_id = Number(ev.target.id)
        console.log(movie_id)
        submit_async_sims_request(movie_id)
    });
})
