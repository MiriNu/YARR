﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Mathematics;

public class ItemFactory : ObjectFactory
{
    protected override void ModifyLevelSettings()
    {
        int level = GetLevel();
        Damage = 0;
        Speed = 0;
        SpawnRateRange = new int2(10, 20);

        // Level properties initialization 
        float[] LevelsOf_DestroyTimer = { -1f, 10f, 7f, 5f, 5f, 5f };
        float2[] LevelsOf_SpawnHeightRange = new float2[]
        {
            new float2(-3, -2), new float2(-3, 0), new float2(-3, 2), new float2(0, 2), new float2(0, 3.5f), new float2(1, 3.5f)
        };

        // Static
        if (level != 0)
        {
            DestroyTimer = LevelsOf_DestroyTimer[level];
            SpawnHeightRange = LevelsOf_SpawnHeightRange[level];
        }
        // Adaptive
        else
        {

        }
    }

    protected override void Spawn()
    {
        const int itemLayer = 10;
        // Calculate a random location to spawn at
        Vector3 position = new Vector3(UnityEngine.Random.Range(-10, 10), UnityEngine.Random.Range(SpawnHeightRange.x, SpawnHeightRange.y), 0);

        // Create an item
        GameObject itemObj = Instantiate(GetPrefab(), position, transform.rotation);
        itemObj.layer = itemLayer;
        itemObj.GetComponent<SpriteRenderer>().sprite = GetSprite();
        itemObj.GetComponent<Treasure>().TreasureInit(GetID(), DestroyTimer);
    }

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(StartSpawner());
    }

    // Update is called once per frame
    void Update()
    {
        // TODO
    }
}
