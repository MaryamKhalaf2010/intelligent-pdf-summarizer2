// Location for all resources  
param location string = 'East US'

// Function Plan SKU and Tier (Flex Consumption Plan)
@description('The SKU name for the App Service plan (e.g., FC1 for Flex Consumption)')
param functionPlanSku string = 'FC1'

@description('The SKU tier for the App Service plan (FlexConsumption for FC1)')
param functionPlanTier string = 'FlexConsumption'

// Generate unique names based on resource group and location
var storageName = 'sumstrg${uniqueString(resourceGroup().id, location)}'
var functionAppName = 'summarizerfunc${uniqueString(resourceGroup().id, location)}'
var hostingPlanName = 'summarizerplan${uniqueString(resourceGroup().id, location)}'

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

// Hosting Plan (Flex Consumption Plan)
resource hostingPlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: hostingPlanName
  location: location
  sku: {
    name: functionPlanSku // FC1
    tier: functionPlanTier // FlexConsumption
  }
  kind: 'elastic'
  properties: {
    reserved: true
  }
}

// Function App using functionAppConfig
resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: hostingPlan.id
    functionAppConfig: {
      runtime: {
        name: 'python'
        version: '3.10'
      }
      bindings: []
      deployment: {
        storage: {
          type: 'zip'
        }
      }
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: storageAccount.properties.primaryEndpoints.blob
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
  }
  tags: {
    'azd-service-name': 'api'
  }
}

output functionAppName string = functionApp.name
output storageAccountName string = storageAccount.name
