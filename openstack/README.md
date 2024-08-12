# UFCity - OpenStack Infrastructure Configuration



<div class="view">
<img src="https://makleyston-ufc.github.io/ufcity/assets/img/ufcity-logo.png" alt="UFCity" width="200"/>
<p><b>Building smart cities smartly.</b></p>
</div>
<div class="view">
  <a href="https://makleyston-ufc.github.io/ufcity/"> <img src="https://img.shields.io/badge/UFCity_webpage-0076D6?style=for-the-badge&logo=internetexplorer&logoColor=white"> </a>
  <a href="https://github.com/makleyston-ufc/ufcity-cloud-computing/tree/main/ufcity-ai-models-samples"> <img src="https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white"> </a>
</div>



## Setting up infrastructure via DevStack

The ```local.conf``` file used in this prototype is available in the [project repository](https://github.com/makleyston-ufc/ufcity-cloud-computing/tree/main/openstack).

<div id="local-conf-content"></div>
<script>
fetch('https://github.com/makleyston-ufc/ufcity-cloud-computing/blob/main/openstack/local.conf')
  .then(response => response.text())
  .then(data => {
    document.getElementById('local-conf-content').textContent = data;
  });
</script>

