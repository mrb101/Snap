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

// Deliverd Car
$(document).on('click', '#deliverd', function(e) {
    e.preventDefault();
    const element = $(this);
    const booking_id = element.attr("value");
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: 'POST',
        url: '/book/' + booking_id + '/deliver/',
        data: {
            booking: booking_id,
            csrfmiddlewaretoken: csrfToken,
        },
        success: (res) => {
            console.log("done!");
        }
    })
});


// Car return
$(document).on('click', '#return', function(e) {
    e.preventDefault();
    const element = $(this);
    const booking_id = element.attr("value");
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: 'POST',
        url: '/book/' + booking_id + '/return/',
        data: {
            booking: booking_id,
            csrfmiddlewaretoken: csrfToken,
        },
        success: (res) => {
            console.log("done!");
        }
    })
});

// Register
$(document).on('submit', '#registerForm', function(e) {
    e.preventDefault();
    console.log("in");
    const username = $('input[name=name]').val();
    const email = $('input[name=email]').val();
    const phone = $('input[name=phone]').val();
    const password1 = $('input[name=password1]').val();
    const password2 = $('input[name=password2]').val();
    $.ajax({
        type: 'POST',
        url: '/register/',
        data: {
            username = username,
            email = email,
            phone = phone,
            password1 = password1,
            password2 = password2,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: (res) => {
            console.log("done!")
        }
    })
});
