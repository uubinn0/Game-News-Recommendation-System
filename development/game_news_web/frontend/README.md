# frontend

## Installing Node.js in a Python Project


### Install nvm (Node Version Manager)
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```

### After installation, set up environment variables:
```
source ~/.bashrc   # for bash
# or
source ~/.zshrc    # for zsh
```

### Verify nvm installation::
```
nvm --version
```


## Install Node.js

### Install the latest version:
```
npm run lint
```
### Verify Node.js installation:
```
node -v
```

## init vue

### Install Vue Cli
```
npm install -g @vue/cli
```

### create vue and add vuetify
```
vue create .
vue add vuetify
```


## Issue : Allowed Hosts Problem in Vue

When making API requests in a Vue application, a `CORS` error may occur due to issues with `Allowed Hosts`. This problem arises when the client sends requests to a different domain than the one it was served from.

## Solution

1. Open the `vue.config.js` file in your Vue project.
2. Add the `allowedHosts: "all"` setting to allow requests from all hosts.
   ```js
   module.exports = {
     devServer: {
       allowedHosts: "all",
     },
   }