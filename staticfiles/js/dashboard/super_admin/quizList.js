import { getData } from '../../Api.js';  // Correct relative import path

function fetchUser() {
    getData('super_admin/super_admin-question-list/')
      .then(data => {
        console.log('Fetched data:', data);  // Handle the fetched data
      })
      .catch(error => {
        console.error('Error fetching data:', error);  // Handle the error
      });
}

fetchUser(); 
