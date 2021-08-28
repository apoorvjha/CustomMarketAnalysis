function loadEntity(){
    var n_entities=document.getElementById('n_entities').value;
    var i=0;
    var entity=document.getElementById('entity');
    for(;i<n_entities;i++){
        entity.innerHTML+='<label>Name</label><input type="text" name="Name'+i+'"><br>';
        entity.innerHTML+='<label>Price</label><input type="text" name="Price'+i+'"><br>';
        entity.innerHTML+='<label>Volume</label><input type="text" name="Volume'+i+'"><br>';
    }
}

function loadUsers(){
    var n_users=document.getElementById('n_users').value;
    var i=0;
    var user=document.getElementById('user');
    for(;i<n_users;i++){
        user.innerHTML+='<label>Seed</label><input type="number" name="seed'+i+'" required><br>';
    }
}