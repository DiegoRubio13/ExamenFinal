using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;

[Serializable]
public class Vector3Data
{
    public float x;
    public float y;
    public float z;

    public Vector3 ToVector3()
    {
        return new Vector3(x, y, z);
    }
}

[Serializable]
public class AgentState
{
    public Vector3Data position;
    public Vector3Data[] path;
    public int[][] grid;
}

[Serializable]
public class ServerResponse
{
    public AgentState[] agents;
}

public class AgentController : MonoBehaviour
{
    public float moveSpeed = 5f;
    public GameObject agentPrefab;
    private GameObject[] agentObjects;
    private string serverUrl = "http://localhost:8585";
    private float updateInterval = 0.1f;
    private GridVisualizer gridVisualizer;
    private bool isGridInitialized = false;

    void Start()
    {
        gridVisualizer = GetComponent<GridVisualizer>();
        if (gridVisualizer == null)
        {
            Debug.LogError("No se encontró el componente GridVisualizer");
        }
        StartCoroutine(UpdateAgents());
    }

    IEnumerator UpdateAgents()
    {
        while (true)
        {
            using (UnityWebRequest www = UnityWebRequest.Get(serverUrl))
            {
                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.Success)
                {
                    string json = www.downloadHandler.text;
                    Debug.Log($"Respuesta del servidor: {json}");

                    ServerResponse response = JsonUtility.FromJson<ServerResponse>(json);

                    if (response.agents != null && response.agents.Length > 0)
                    {
                        
                        if (!isGridInitialized && response.agents[0].grid != null)
                        {
                            Debug.Log("Inicializando grid desde el servidor");
                            UpdateGrid(response.agents[0].grid);
                            isGridInitialized = true;
                        }

                        
                        if (agentObjects == null || agentObjects.Length != response.agents.Length)
                        {
                            if (agentObjects != null)
                            {
                                foreach (var obj in agentObjects)
                                {
                                    Destroy(obj);
                                }
                            }
                            agentObjects = new GameObject[response.agents.Length];
                            for (int i = 0; i < response.agents.Length; i++)
                            {
                                agentObjects[i] = Instantiate(agentPrefab, Vector3.zero, Quaternion.identity);
                            }
                        }

                       
                        for (int i = 0; i < response.agents.Length; i++)
                        {
                            var agent = response.agents[i];
                            var targetPos = agent.position.ToVector3();

                          
                            if (agentObjects[i] != null)
                            {
                                agentObjects[i].transform.position = Vector3.Lerp(
                                    agentObjects[i].transform.position,
                                    targetPos,
                                    moveSpeed * Time.deltaTime
                                );

                                
                                if (agent.path != null && agent.path.Length > 1)
                                {
                                    int currentPathIndex = 0;
                                   
                                    for (int j = 0; j < agent.path.Length - 1; j++)
                                    {
                                        if (Vector3.Distance(agentObjects[i].transform.position, agent.path[j].ToVector3()) < 0.1f)
                                        {
                                            currentPathIndex = j;
                                            break;
                                        }
                                    }

                                    if (currentPathIndex < agent.path.Length - 1)
                                    {
                                        Vector3 nextPos = agent.path[currentPathIndex + 1].ToVector3();
                                        Vector3 direction = (nextPos - agentObjects[i].transform.position).normalized;
                                        if (direction != Vector3.zero)
                                        {
                                            agentObjects[i].transform.rotation = Quaternion.Lerp(
                                                agentObjects[i].transform.rotation,
                                                Quaternion.LookRotation(direction),
                                                moveSpeed * Time.deltaTime
                                            );
                                        }
                                    }
                                }
                            }
                        }
                    }
                    else
                    {
                        Debug.LogWarning("No se recibieron datos de agentes del servidor");
                    }
                }
                else
                {
                    Debug.LogError($"Error en la petición: {www.error}");
                }
            }

            yield return new WaitForSeconds(updateInterval);
        }
    }

    void UpdateGrid(int[][] gridArray)
    {
        if (gridArray == null)
        {
            Debug.LogError("Grid array es nulo");
            return;
        }

        Debug.Log($"Recibido grid de dimensiones: {gridArray.Length}x{gridArray[0].Length}");

        int rows = gridArray.Length;
        int cols = gridArray[0].Length;
        int[,] grid = new int[rows, cols];

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                grid[i, j] = gridArray[i][j];
            }
        }

        if (gridVisualizer != null)
        {
            gridVisualizer.UpdateGrid(grid);
        }
        else
        {
            Debug.LogError("GridVisualizer no encontrado");
        }
    }
}