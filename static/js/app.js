// Book a car
$(document).on('submit', '#addBooking', (e) => {
    e.preventDefault();
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val()

    const category = $('#id_category').val();
    const address = $('#id_address').val();
    const starts = $('#id_starts').val();
    const duration= $('#id_duration').val();
    $.ajax({
        type: 'POST',
        url: '/booking/new/',
        data: {
            category: category,
            address: address,
            starts: starts,
            duration: duration,
            csrfmiddlewaretoken: csrfToken,
        },
        success: (res) => {
            const response = JSON.parse(res);
            const type = response.type;
            const msg = response.msg;
            const category = response.category;
            const starts = response.starts;
            const duration = response.duration;
            console.log(msg)
        },
        error: (res) => {
            console.log(res)
        }
    })
});


// Confirm booking
$(document).on('click', '#accept', function(e) {
    e.preventDefault();
    const element = $(this);
    const booking_id = element.attr("value");
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    console.log(csrfToken)
    $.ajax({
        type: 'POST',
        url: '/book/' + booking_id + '/confirm/',
        data: {
            booking: booking_id,
            csrfmiddlewaretoken: csrfToken,
        },
        success: (res) => {
        console.log("done!");
        }
    })
});
