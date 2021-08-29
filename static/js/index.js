function loadEntity(){
    var n_entities=document.getElementById('n_entities').value;
    var i=0;
    var entity=document.getElementById('entity');
    entity.innerHTML='<h3>&nbsp;&nbsp;&nbsp;Entity Information</h3><br><br>';
    for(;i<n_entities;i++){
        entity.innerHTML+='&nbsp;&nbsp;&nbsp;<label>Name</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" name="Name'+i+'">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small id="" class="text-muted"><font color="blue">Enter Name of Entity '+String(i+1)+'!</font></small><br>';
        entity.innerHTML+='&nbsp;&nbsp;&nbsp;<label>Price</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" name="Price'+i+'">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small id="" class="text-muted"><font color="blue">Enter Price of Entity '+String(i+1)+'!</font></small><br>';
        entity.innerHTML+='&nbsp;&nbsp;&nbsp;<label>Volume</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="text" name="Volume'+i+'">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small id="" class="text-muted"><font color="blue">Enter Volume of Entity '+String(i+1)+'!</font></small><br><br>';
    }
}

function loadUsers(){
    var n_users=document.getElementById('n_users').value;
    var i=0;
    var user=document.getElementById('user');
    user.innerHTML='<h3>&nbsp;&nbsp;&nbsp;Player Information</h3><br><br>'
    for(;i<n_users;i++){
        user.innerHTML+='&nbsp;&nbsp;&nbsp;<label>Seed</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" name="seed'+i+'" required>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small id="" class="text-muted"><font color="blue">Enter Seed investment of Player '+String(i+1)+'!</font></small><br><br>';
    }
}