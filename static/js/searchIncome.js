const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const noResults = document.querySelector('.no-results')
const tBody = document.querySelector('.table-body')
const pagContainer = document.querySelector('.pagination-container')


tableOutput.style.display = 'none'
noResults.style.display = 'none'
searchField.addEventListener('keyup', (e) => {

    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        pagContainer.style.display = 'none'
        tBody.innerHTML = ''
        fetch("search-income/", {
        body: JSON.stringify({ searchText: searchValue }),
        method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                appTable.style.display = 'none'
                tableOutput.style.display = 'block'
                noResults.style.display = 'none'
               if(data.length===0){
                    noResults.style.display = 'block'
                   tableOutput.style.display = 'none'
               }
               else{
                   data.forEach(item=>{
                     tBody.innerHTML +=`
                   <tr style="font-size: 17px">
                   <td>${item.amount}</td>
                   <td>${item.source}</td>
                   <td>${item.description}</td>
                   <td>${item.date}</td>
                   <td><a style="margin-right: 15px" href="income/edit-income/${item.id}" class="btn btn-secondary btn-sm">Edit</a>
                       <a href="income/delete-income/${item.id}" class="btn btn-danger btn-sm">Delete</a></td>
                    </tr>
                   `
                   })
               }
            })
    }else{
        appTable.style.display = 'block'
        tableOutput.style.display = 'none'
        noResults.style.display = 'none'
        pagContainer.style.display = 'block'
    }
})