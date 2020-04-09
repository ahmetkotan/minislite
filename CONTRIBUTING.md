# MiniSLite Development and Contribution

#### Open issue
Open issue about your feature or bug in this [here](https://github.com/ahmetkotan/minislite/issues).
#### Clone this repository.
```
git clone https://github.com/ahmetkotan/minislite
```
#### Create new branch with your issue id
```
git checkout -b feature-#<issue-id>
```
#### Install Requirements
```
pip install -r requirements/development.txt
```
#### Make your changes
#### Write tests
#### Pre-commit
```
pre-commit install
```
#### Commit and push your changes
```
git add .
pre-commit run  # check pre-commit
git commit -m "added changes #<issue-id>"
git push origin feature-#<issue-id>
```
#### Create new Pull Request
