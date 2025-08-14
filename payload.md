# OpenAI API Payload

**Pricing Tier:** flex

```json
{
  "model": "gpt-5",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert image analyst with a keen eye for detail and visual aesthetics. Carefully review the provided image in depth. Examine all visible elements. Consider both content and aesthetics, and describe each observation objectively and based only on visual evidence. Return your findings in a single, valid JSON object with clear, descriptive keys for each aspect of the analysis. Use detailed, specific language to convey the nuances of your observations. Do not include any lead-in, introduction, commentary, summary, or outro. Your output must be purely the JSON object."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://www.usatoday.com/gcdn/-mm-/1fecae5856e58374cc9e1c0fd6dcc3c6aae79d4e/c=0-293-5760-3547/local/-/media/USATODAY/None/2014/10/27/635500305294949597-XXX-INTERSTELLAR-MOV-JY-3194--67833286.JPG"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 1024,
  "response_format": {
    "type": "json_object"
  },
  "_pricing_tier": "flex"
}
```
