$(document).foundation()


$(document).on('submit', '#addBooking', (e) => {
    e.preventDefault()
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val()
    const category = $('#id_category').val();
    const starts = $('#id_starts').val();
    const duration = $('#id_duration').val();
    $.ajax({
        type: 'POST',
        url: '/booking/new/',
        data: {
            category: category,
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
})
