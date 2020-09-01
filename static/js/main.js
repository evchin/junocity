$(document).ready(function() {

  // hamburger menu toggle

  $('.nav-toggle').click(function() {
    $('.nav').toggleClass('is-open');
    $('.hamburger').toggleClass('is-open');
    $('.go-left').toggleClass('is-open');
    $('#postman').toggleClass('is-open');
    $('.block-nav-toggle').removeClass('is-open');
    $('.block-nav-toggle').toggleClass('nav-open');
    $('.block-list').removeClass('is-open');
    $('.inbox-nav-toggle').removeClass('is-open');
    $('.inbox-nav-toggle').toggleClass('nav-open');
    $('#postman_menu').removeClass('is-open');
  })

  $('.nav-link').click(function(){
    $('.nav').removeClass('is-open');
    $('.hamburger').removeClass('is-open');
  })

  $('.block-nav-toggle').click(function() {
    $('.block-list').toggleClass('is-open');
    $('.block-hamburger').toggleClass('is-open');
    $('.nav').removeClass('is-open');
    $('.hambuger').removeClass('is-open');
  })

  $('.inbox-nav-toggle').click(function() {
    $('#postman_menu').toggleClass('is-open');
    $('.inbox-hamburger').toggleClass('is-open');
    $('.nav').removeClass('is-open');
    $('.hamburger').removeClass('is-open');
  })

  // browse filter

  $('.filter-button').click(function(){
    $(".filter-button").removeClass("selected-filter");
    $(".results-grid").removeClass("selected-filter");
    $(this).addClass("selected-filter");
    el = document.querySelector('#' + this.id + '-grid-id')
    $(el).addClass('selected-filter');
  })

  // add bookmark

  $('.bookmark-form').submit(function(event){
      event.preventDefault() 
      event.stopPropagation()
      var $formData = $(this).val()
      var postData = {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()}
      var $thisURL = $(this).attr('data-url') || window.location.href 
      var form_action =  $(this).attr('action')
      $.ajax({
          method: "POST",
          url: form_action,
          data: postData,
          success: function (data) {console.log('I work')},
          error: function(data) {console.log("Something went wrong!");}
      })
      return false; 
  })

  // change post like

  $('.like-form').submit(function(event){
        event.preventDefault() 
        pk = event.originalEvent.srcElement.elements[1].value
        var $formData = $(this).val()
        var postData = {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()}
        var $thisURL = $(this).attr('data-url') || window.location.href 
        var form_action =  $(this).attr('action')
        $.ajax({
            method: "POST",
            url: form_action,
            data: postData,
            success: function(data) {console.log(data)},
            error: function(data) {console.log("Something went wrong!");}
        })
        return false;
    })

    // fade toggle comment replies

    $(".reply-link").click(function(event) {
        event.preventDefault();
        $(this).parent().next(".replies").fadeToggle();
    })

  // csrf token
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})

// change bookmark image
function changeBookmark(id) {
    el = document.querySelector('#' + id)
    source = el.src
    if (source.substring(source.length - 13) == "/bookmark.svg" || 
        source.substring(33, 46) == "/bookmark.svg") {
        el.src = 'https://junocity.s3-us-west-1.amazonaws.com/is-bookmark.svg';
        console.log(el.src)
    } else {
        el.src = 'https://junocity.s3-us-west-1.amazonaws.com/bookmark.svg';
        console.log(el.src)
    }
}

// change like image
function changeLike(id) {
    el = document.querySelector('#' + id)
    source = el.src
    if (source.substring(source.length - 22) == "/like-button-liked.svg" || 
        source.substring(33, 55) == "/like-button-liked.svg") {
        el.src = 'https://junocity.s3-us-west-1.amazonaws.com/like-button.svg';
        console.log(el.src)
    } else { 
        el.src = 'https://junocity.s3-us-west-1.amazonaws.com/like-button-liked.svg';
        console.log(el.src)
    }
}