// window.onload = function() {
//
//     // Hide the loader image and show some instructions
//     $("#loader").hide();
//     $('#images').html(`
// 		<div>
//     		<h2 class="center">Click on any image. Similar images appear below...</h2>
// 		</div>`).show();
//
//     // Show the thumbnails
//     $("#row_of_thumbnails").css("display", "block");
// }










// $(document).ready shortcut you should use instead of $(document).ready
// This code is responsble for submitting async requests on clicks of state / month
$(() => {
    // // When clicking month, trigger backend request with month and state
    // $('input[type=radio]').change( function() {
    //     const month = $('[name="button"]:checked').val()
    //     submit_async_request(selectedState, month)
    // });
    //
    // $(document).on('submit', '#form', (ev) => {
    //     ev.preventDefault()
    //     const state = $('#state').val()
    //     const month = $('#month').val()
    //     submit_async_request(state, month)
    // });
    //
    // $(document).on('reset', '#form', (ev) => {
    //     ALL_DATA = [];
    //     render(ALL_DATA);
    // })

    $(document).on('click', '.rounded-circle', (ev) => {
        ev.preventDefault()
        const userId = Number(ev.target.id)
        submit_async_request(userId)
    })
})






async function submit_async_request(userId) {
    // Execute POST request
    const response = await fetch('/rec_predict', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': userId
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        renderError();
        return
    }
    const data = await response.json();
    console.log(data);
    render(data)
    // ALL_DATA.unshift(data);
    // ALL_DATA = ALL_DATA.slice(0, 10);
    // render(ALL_DATA)
}


function renderError() {
    $('#errorAlert').text('Oooopsies. There was an issue with this user.').show();
    $('#successAlert').hide();
}

function render(results) {
    $('#errorAlert').hide();

    $('#rec_results')
        // equivalent to python lambda function
        .html(results.map(result => renderResult(result)).join(''))
        .show()
}

// Generate Formatted HTML to show subcategories
function renderResult(data) {
    const {
        recs,
        state,
        month
    } = data

    const rows = recs.slice(0, 10)

    return `
        <div class="col-sm-3">
            <h2 class="table_title">${state} in ${month}</h2>
            <table class="table" id="results_table">
                <thead>
                    <tr>
                      <th>Superclass</th>
                      <th>Subcategory</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows.map(row => `<tr><td>${row.split('=')[1].split(' ::')[0]}</td><td>${row.split('=')[1].split(':: ')[1]}</td>`).join('')}
                </tbody>
            </table>
        </div>
    `;
}
