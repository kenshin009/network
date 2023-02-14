const submit__btn = document.querySelector('#submit')
        const content = document.querySelector('#content')
        content.addEventListener('input',() => {
            if(content.value.length > 0 && content.value.trim() !== '') {
                submit__btn.disabled = false;
            } else {
                submit__btn.disabled = true;
            }
        })

        document.querySelector('#like').addEventListener('click',handleClick)

        function handleClick() {
            let likes = parseInt(document.querySelector('#like_count').innerHTML) 
            if (likes === 0 ) {
                // Change heart icon
                document.querySelector('#heart').className = 'bi bi-heart-fill'
                const post_id = document.querySelector('#post_id').value
                const user = document.querySelector('#user').value
                const newLike = {
                        id: 1,
                        post_id: post_id,
                        user: user
                    }

                // Fetch like-posts url and create new like
                fetch('/like-posts',{
                    method: 'POST',
                    body: JSON.stringify(newLike),
                })
                .then((res) => res.json())
                .then((data) => {
                   console.log(data)
                })
                .catch((err) => console.log(err))

                // Get the liked post
                const liked_post = {
                    "id": post_id
                }
                // Fetch post_detail url and increment likes using put method
                fetch(`/posts/${post_id}`,{
                    method: 'PUT',
                    body: JSON.stringify(liked_post)
                })
                .then((res) => res.json())
                .then((data) => {
                    {
                        // Show total likes in dom
                        document.querySelector('#like_count').innerHTML = data['likes']
    
                    }
                })
                .catch((err) => console.log(err))

            } else {
                const post_id = document.querySelector('#post_id').value
                const user = document.querySelector('#user').value
                // Filter likes of the liked post using fetch
                fetch(`/like-post-detail/${post_id}`)
                .then((res) => res.json())
                .then((data) => {
                    // Check this user has already liked this post or not
                    data.response.forEach((like) => {
                        
                        if (like.user === user) {
                            
                        // already liked the post
                        // change the heart icon
                        document.querySelector('#heart').className = 'bi bi-heart'
                        // Get specific like obj
                        const like_obj = {
                            "post_id": post_id,
                            "user": user
                        }
                        // Fetch put to remove like and decrement like count by 1
                        fetch(`/like-post-detail/${post_id}`,{
                        method: 'PUT',
                        body: JSON.stringify(like_obj),
                        })
                        .then((res) => res.json())
                        .then((data) => {
                            // Show the total likes in dom
                            document.querySelector('#like_count').innerHTML =  data['likes']
                            console.log(data)
                        })
                        .catch((err) => console.log(err))

                        } else { 
                            
                        // Have not liked the post
                        // Change the heart icon
                        document.querySelector('#heart').className = 'bi bi-heart-fill'
                        // Get specific like obj
                         const like_obj = {
                            "post_id": post_id,
                            "user": user
                        }
                        // Fetch put to create new like and increment like count by 1
                        fetch(`/like-post-detail/${post_id}`,{
                        method: 'PUT',
                        body: JSON.stringify(like_obj),
                        })
                        .then((res) => res.json())
                        .then((data) => {
                            // Show the total likes in dom
                          
                            document.querySelector('#like_count').innerHTML =  data['likes']
                           
                        })
                        .catch((err) => console.log(err))

                        }
                    })
                        
                  
                })
            }
        }