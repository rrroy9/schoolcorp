$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('click', '.like-link', function(event) {
        event.preventDefault();
        var postId = $(this).data("post-id");
        var url = $(this).data("url");
        var likeLink = $(this);

        $.ajax({
            type: "POST",
            url: url,
            data: {
                post_id: postId
            },
            success: function(data) {
                var newContent = `
                    <span class="likes-count">${data.likes_count}</span>
                    <a href="#" class="like-button like-link" data-post-id="${postId}" data-url="${url}">
                        <?xml version="1.0" encoding="utf-8"?>
                        <svg width="20" height="20" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                            <path d="M320 1344q0-26-19-45t-45-19q-27 0-45.5 19t-18.5 45q0 27 18.5 45.5t45.5 18.5q26 0 45-18.5t19-45.5zm160-512v640q0 26-19 45t-45 19h-288q-26 0-45-19t-19-45v-640q0-26 19-45t45-19h288q26 0 45 19t19 45zm1184 0q0 86-55 149 15 44 15 76 3 76-43 137 17 56 0 117-15 57-54 94 9 112-49 181-64 76-197 78h-129q-66 0-144-15.5t-121.5-29-120.5-39.5q-123-43-158-44-26-1-45-19.5t-19-44.5v-641q0-25 18-43.5t43-20.5q24-2 76-59t101-121q68-87 101-120 18-18 31-48t17.5-48.5 13.5-60.5q7-39 12.5-61t19.5-52 34-50q19-19 45-19 46 0 82.5 10.5t60 26 40 40.5 24 45 12 50 5 45 .5 39q0 38-9.5 76t-19 60-27.5 56q-3 6-10 18t-11 22-8 24h277q78 0 135 57t57 135z"/>
                        </svg>
                    </a>
                `;
                $("#like-" + postId).html(newContent);
                // Trigger animation after updating content
                animateButton($("#like-" + postId).find('.like-button'));
            }
        });
    });

    function animateButton(button) {
        button.toggleClass("active");
        button.addClass("animated");
        generateClones(button[0]);
    }

    function generateClones(button) {
        let clones = randomInt(2, 4);
        for (let it = 1; it <= clones; it++) {
            let clone = button.querySelector("svg").cloneNode(true),
                size = randomInt(5, 16);
            button.appendChild(clone);
            clone.setAttribute("width", size);
            clone.setAttribute("height", size);
            clone.style.position = "absolute";
            clone.style.transition =
                "transform 0.5s cubic-bezier(0.12, 0.74, 0.58, 0.99) 0.3s, opacity 1s ease-out .5s";
            let animTimeout = setTimeout(function() {
                clearTimeout(animTimeout);
                clone.style.transform =
                    "translate3d(" +
                    (plusOrMinus() * randomInt(10, 25)) +
                    "px," +
                    (plusOrMinus() * randomInt(10, 25)) +
                    "px,0)";
                clone.style.opacity = 0;
            }, 1);
            let removeNodeTimeout = setTimeout(function() {
                clone.parentNode.removeChild(clone);
                clearTimeout(removeNodeTimeout);
            }, 900);
            let removeClassTimeout = setTimeout(function() {
                button.classList.remove("animated");
            }, 600);
        }
    }

    function plusOrMinus() {
        return Math.random() < 0.5 ? -1 : 1;
    }

    function randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }
});


$(document).ready(function() {
    $('#comment-form').submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var formData = form.serialize();
        var url = form.attr('action');
        var postId = form.data('post-id'); // Get the post ID from the data attribute

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(data) {
                // Add the new comment to the specific post's comment list
                var commentHtml = '<li>' +
                                    '<div class="comet-avatar">' +
                                        '<img src="' + data.user_profile_pic + '" alt="">' +
                                    '</div>' +
                                    '<div class="we-comment">' +
                                        '<div class="coment-head">' +
                                            '<h5><a title="">' + data.user_first_name + ' ' + data.user_last_name + '</a></h5>' +
                                            '<span>' + data.date_added + '</span>' +
                                        '</div>' +
                                        '<p>' + data.comment_body + '</p>' +
                                    '</div>' +
                                '</li>';
                $('#comments-' + postId).find('.we-comet').append(commentHtml);
                // Clear the form
                form.find('textarea').val('');
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});