let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

if(searchForm){
    for(let i=0;pageLinks.length>i;i++){
        pageLinks[i].addEventListener('click', function(e){
            e.preventDefault()
            let page = this.dataset.page
            searchForm.innerHTML += `<input value=${page} name="page" hidden>`
            searchForm.submit()
        });
    }
}


let tags = document.getElementsByClassName("project-tag")

if(tags){
    for(let i=0; tags.length>i;i++){
            tags[i].addEventListener('click',(e)=>{
                tagId=e.target.dataset.tag
                blogId=e.target.dataset.blog

                fetch(`http://127.0.0.1:8000/api/remove-tag/`,{
                method:'DELETE',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify({'tag':tagId,"blog":blogId})

                })
                .then(response => response.json())
                .then(data =>{
                    e.target.remove()
                })
                })
        }
}


const date = new Date()
let date_time = document.getElementById("date-time")
let year = date.getFullYear();

date_time.innerHTML = `&#169; BlogEx | ${year}`