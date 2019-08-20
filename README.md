# kent-risk-analysis


## Usage
```
docker-compose up 
```

Once the 3 Docker containers have been built and launched, a web server will be listening on http://localhost:4242.  
From there:
* Add some products to your basket
* Checkout
* Fill out the form with fake information (we haven't started a true business yet ...)
    * Note somewhere the credit card number, as it is used to identify your profile and let the AI validate it on subsequent purchases
* As you will see from Docker logs, the AI will detect a new profile from your credit card, thus triggering a challenge to validate your identity

If you repeat the same process with the same credit card number, the AI should match received fingerprint with the previous one and so validate your purchase without further challenge.
