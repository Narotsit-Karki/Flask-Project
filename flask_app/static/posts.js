function like(postId){
        const likecount = document.getElementById('like-count-'+(postId).toString());
        const likebutton = document.getElementById('like-button-${postId}');
        console.log(likecount.innerHTML);
        fetch("/like-post/"+(postId).toString(), {method:'POST'})
        .then( (res) => res.json())
        .then((data) => {
            likecount.innerHTML = "Liked by " + (data['likes']).toString() + " people";
            });
    }

var myHand = false;
function startAni(elem,postId) {
     like(postId);
    if (myHand)
        clearTimeout(myHand);

    myHand = setTimeout(function(){animate(elem,postId);}, 250);

    elem.style.animation = "fa-pulse-click 0.2s ease";
    }

    function animate(elem,postId) {

    elem.style.animation = '';
    elem.classList.toggle("fa-heart-o");
    elem.classList.toggle("fa-heart");

}
   