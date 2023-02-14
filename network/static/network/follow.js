document.querySelector('#follow_btn').addEventListener('click',handleClick)

function handleClick() {
    // Check how many followers have
   const follower_count = parseInt(document.querySelector('#follower_count').innerHTML)
    // Create new follow obj 
    const new_follow = {
        "user_follow": document.querySelector('#user_follow').value,
        "user_profile": document.querySelector('#user_profile').value
    }
   // if there is no followers
   if (follower_count === 0) {
      
        // Use the data to create new follow model using FETCH POST
        fetch('/follows',{
            method: 'POST',
            body: JSON.stringify(new_follow)
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            document.querySelector('#follower_count').innerHTML = data['profile_follower']
            if (data['already_followed'] != '') {
                document.querySelector('#follow_btn').innerHTML = "Unfollow"
            } else {
                document.querySelector('#follow_btn').innerHTML = "Follow"
            }
        })
        .catch(err => console.log(err))
   } else {
    // if there is one or more followers
    // Use the data to update follow model using FETCH PUT
    fetch('/follows',{
        method: 'PUT',
        body: JSON.stringify(new_follow)
    })
    .then(res=>res.json())
    .then(data=> {
        console.log(data)
        document.querySelector('#follower_count').innerHTML = data['profile_follower']
        if (data['already_followed'] == true) {
            document.querySelector('#follow_btn').innerHTML = "Unfollow"
        } else {
            document.querySelector('#follow_btn').innerHTML = "Follow"
        }
    })
   }
}